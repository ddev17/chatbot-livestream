from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from model.LLMBotResCmt import LLMBotResCmt

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls

# Initialize chatbot
Chatbot_Res_CMT = LLMBotResCmt()

# Cache for HTML content
html_content = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Livestream Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f5;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }

        .tabs {
            display: flex;
            margin-bottom: 20px;
            gap: 10px;
        }

        .tab {
            background: white;
            border: none;
            padding: 15px 30px;
            cursor: pointer;
            border-radius: 10px 10px 0 0;
            transition: all 0.3s;
            font-weight: bold;
            color: #666;
        }

        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .tab-content {
            background: white;
            border-radius: 0 10px 10px 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            min-height: 500px;
        }

        .tab-pane {
            display: none;
        }

        .tab-pane.active {
            display: block;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            height: 500px;
        }

        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-content {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 18px;
            background: #e9ecef;
            animation: fadeIn 0.3s ease-in;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Typing indicator animation */
        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 10px 15px;
            background: #e9ecef;
            border-radius: 18px;
            max-width: 80px;
        }

        .typing-indicator span {
            height: 8px;
            width: 8px;
            background: #666;
            border-radius: 50%;
            display: inline-block;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }

        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 60%, 100% {
                opacity: 0.3;
                transform: scale(0.8);
            }
            30% {
                opacity: 1;
                transform: scale(1.2);
            }
        }

        /* Loading spinner for comments */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102, 126, 234, 0.3);
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
            vertical-align: middle;
            margin-right: 8px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .chat-input {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
        }

        input:focus {
            border-color: #667eea;
        }

        button {
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: scale(0.98);
        }

        /* Ripple effect for buttons */
        button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        button:active::after {
            width: 300px;
            height: 300px;
        }

        .livestream-container {
            display: flex;
            flex-direction: column;
            height: 500px;
        }

        .livestream-input {
            margin-bottom: 20px;
        }

        .comment-list {
            flex: 1;
            overflow-y: auto;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }

        .comment {
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .comment-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }

        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #667eea;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin-right: 10px;
        }

        .nickname {
            font-weight: bold;
            color: #667eea;
        }

        .comment-content {
            margin-bottom: 10px;
        }

        .bot-response {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            border-left: 3px solid #764ba2;
        }

        .status {
            text-align: center;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .status.active {
            background: #d4edda;
            color: #155724;
            position: relative;
        }

        .status.active::before {
            content: '';
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 10px;
            height: 10px;
            background: #dc3545;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.7);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(220, 53, 69, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(220, 53, 69, 0);
            }
        }

        .status.inactive {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Livestream Chatbot Assistant</h1>
            <p>Trả lời khách hàng tự động trong livestream</p>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="switchTab('chat')">💬 Chat với Chatbot</button>
            <button class="tab" onclick="switchTab('livestream')">📺 Livestream Comments</button>
        </div>

        <div class="tab-content">
            <div id="chat-tab" class="tab-pane active">
                <div class="chat-container">
                    <div class="messages" id="chatMessages"></div>
                    <div class="chat-input">
                        <input type="text" id="chatInput" placeholder="Nhập tin nhắn..." onkeypress="handleChatEnter(event)">
                        <button onclick="sendMessage()">Gửi</button>
                    </div>
                </div>
            </div>

            <div id="livestream-tab" class="tab-pane">
                <div class="livestream-container">
                    <div class="livestream-input">
                        <input type="text" id="chatroomId" placeholder="Nhập Chatroom ID (VD: SPIM-EQ9CBC21SRK01)" value="SPIM-EQ9CBC21SRK01">
                        <button onclick="toggleLivestream()">Bắt đầu nhận comments</button>
                    </div>
                    <div class="status inactive" id="livestreamStatus">⏹ Chưa kết nối</div>
                    <div class="comment-list" id="commentList"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isLivestreamActive = false;
        let livestreamInterval = null;
        let lastTimestamp = 0;

        function switchTab(tabName) {
            // Remove active class from all tabs and panes
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            
            // Add active class to selected tab and pane
            if (tabName === 'chat') {
                document.querySelector('.tab:nth-child(1)').classList.add('active');
                document.getElementById('chat-tab').classList.add('active');
            } else {
                document.querySelector('.tab:nth-child(2)').classList.add('active');
                document.getElementById('livestream-tab').classList.add('active');
            }
        }

        function handleChatEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addChatMessage(message, 'user');
            input.value = '';
            
            // Add typing indicator
            const typingId = addTypingIndicator();
            
            // Get bot response
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Remove typing indicator
                removeTypingIndicator(typingId);
                
                // Add bot response with a slight delay for better UX
                setTimeout(() => {
                    addChatMessage(data.response, 'bot');
                }, 100);
            } catch (error) {
                removeTypingIndicator(typingId);
                addChatMessage('Xin lỗi, không thể kết nối với chatbot!', 'bot');
            }
        }

        function addChatMessage(message, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = message;
            
            messageDiv.appendChild(contentDiv);
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function addTypingIndicator() {
            const messagesDiv = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot';
            typingDiv.id = `typing-${Date.now()}`;
            
            const indicatorDiv = document.createElement('div');
            indicatorDiv.className = 'typing-indicator';
            indicatorDiv.innerHTML = '<span></span><span></span><span></span>';
            
            typingDiv.appendChild(indicatorDiv);
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            return typingDiv.id;
        }

        function removeTypingIndicator(typingId) {
            const typingDiv = document.getElementById(typingId);
            if (typingDiv) {
                typingDiv.remove();
            }
        }

        function toggleLivestream() {
            if (isLivestreamActive) {
                stopLivestream();
            } else {
                startLivestream();
            }
        }

        function startLivestream() {
            const chatroomId = document.getElementById('chatroomId').value;
            if (!chatroomId) {
                alert('Vui lòng nhập Chatroom ID!');
                return;
            }
            
            isLivestreamActive = true;
            updateLivestreamStatus(true);
            
            // Fetch comments immediately
            fetchComments(chatroomId);
            
            // Set interval to fetch every 3 seconds
            livestreamInterval = setInterval(() => {
                fetchComments(chatroomId);
            }, 3000);
        }

        function stopLivestream() {
            isLivestreamActive = false;
            updateLivestreamStatus(false);
            
            if (livestreamInterval) {
                clearInterval(livestreamInterval);
                livestreamInterval = null;
            }
        }

        function updateLivestreamStatus(active) {
            const statusDiv = document.getElementById('livestreamStatus');
            const button = document.querySelector('#livestream-tab button');
            
            if (active) {
                statusDiv.className = 'status active';
                statusDiv.textContent = '🔴 Đang nhận comments...';
                button.textContent = 'Dừng nhận comments';
            } else {
                statusDiv.className = 'status inactive';
                statusDiv.textContent = '⏹ Chưa kết nối';
                button.textContent = 'Bắt đầu nhận comments';
            }
        }

        async function fetchComments(chatroomId) {
            try {
                // Use our backend proxy to avoid CORS issues
                const response = await fetch(`/api/shopee/comments/${chatroomId}`);
                const data = await response.json();
                
                if (data.code === 0 && data.data.message) {
                    data.data.message.forEach(messageGroup => {
                        if (messageGroup.timestamp > lastTimestamp) {
                            lastTimestamp = messageGroup.timestamp;
                            
                            messageGroup.msgs.forEach(msg => {
                                const content = JSON.parse(msg.content);
                                if (content.type === 100) {
                                    addComment({
                                        nickname: msg.nickname,
                                        content: content.content,
                                        avatar: msg.avatar,
                                        id: msg.id
                                    });
                                }
                            });
                        }
                    });
                }
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        }

        async function addComment(comment) {
            const commentList = document.getElementById('commentList');
            const commentDiv = document.createElement('div');
            commentDiv.className = 'comment';
            
            const initial = comment.nickname.charAt(0).toUpperCase();
            
            commentDiv.innerHTML = `
                <div class="comment-header">
                    <div class="avatar">${initial}</div>
                    <div class="nickname">${comment.nickname}</div>
                </div>
                <div class="comment-content">${comment.content}</div>
                <div class="bot-response" id="response-${comment.id}">
                    <span class="loading-spinner"></span>
                    <em>Đang suy nghĩ câu trả lời...</em>
                </div>
            `;
            
            // Add fade in animation
            commentDiv.style.animation = 'fadeIn 0.5s ease-in';
            
            commentList.insertBefore(commentDiv, commentList.firstChild);
            
            // Get bot response
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: comment.content })
                });
                
                const data = await response.json();
                
                // Animate the response update
                const responseDiv = document.getElementById(`response-${comment.id}`);
                responseDiv.style.opacity = '0';
                
                setTimeout(() => {
                    responseDiv.innerHTML = `
                        <strong>🤖 Chatbot:</strong> ${data.response}
                    `;
                    responseDiv.style.transition = 'opacity 0.3s ease-in';
                    responseDiv.style.opacity = '1';
                }, 300);
            } catch (error) {
                const responseDiv = document.getElementById(`response-${comment.id}`);
                responseDiv.style.opacity = '0';
                
                setTimeout(() => {
                    responseDiv.innerHTML = `
                        <strong>🤖 Chatbot:</strong> <em>Không thể trả lời lúc này!</em>
                    `;
                    responseDiv.style.transition = 'opacity 0.3s ease-in';
                    responseDiv.style.opacity = '1';
                }, 300);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template_string(html_content)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return bot response"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from chatbot
        bot_response = Chatbot_Res_CMT.predict(user_message)
        
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopee/comments/<chatroom_id>')
def proxy_shopee_comments(chatroom_id):
    """Proxy requests to Shopee API to avoid CORS issues"""
    try:
        url = f"https://chatroom-live.shopee.vn/api/v1/fetch/chatroom/{chatroom_id}/message"
        response = requests.get(url)
        return jsonify(response.json())
    except Exception as e:
        print(f"Error fetching Shopee comments: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/process', methods=['POST'])
def process_comments():
    """Process multiple comments and return bot responses"""
    try:
        data = request.json
        comments = data.get('comments', [])
        
        responses = []
        for comment in comments:
            bot_response = Chatbot_Res_CMT.predict(comment)
            responses.append(bot_response)
        
        return jsonify({'responses': responses})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)