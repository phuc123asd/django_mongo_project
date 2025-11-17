import React, { useEffect, useState, useRef } from 'react';
import { ChatMessage } from '../components/ChatMessage';
import { ChatInput } from '../components/ChatInput';
import { WelcomeScreen } from '../components/WelcomeScreen';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  images?: string[];
}

export function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth'
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async (text: string, images?: File[]) => {
    if (!text.trim() && (!images || images.length === 0)) return;

    // Tạo URL ảnh để hiển thị (nếu có)
    const imageUrls = images ? images.map(img => URL.createObjectURL(img)) : [];
    
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
      timestamp: new Date(),
      images: imageUrls.length > 0 ? imageUrls : undefined,
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Tạo FormData để gửi cả text và file
      const formData = new FormData();
      formData.append('question', text);
      formData.append('role', 'admin'); // Quan trọng: chỉ định role là admin
      
      // Gửi kèm hình ảnh nếu có
      if (images) {
        for (let i = 0; i < images.length; i++) {
          formData.append('images', images[i]);
        }
      }

      // Gọi API đến backend
      // Bỏ đi phần config headers, để Axios tự xử lý
      const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', formData);
      
      // Xử lý phản hồi từ backend
      const responseData = response.data;
      let aiResponseText = '';

      if (responseData.action === "general_chat") {
        aiResponseText = responseData.answer;
      } else if (responseData.success) {
        aiResponseText = responseData.message;
      } else if (!responseData.success) {
        aiResponseText = `❌ ${responseData.error}`;
      } else {
        aiResponseText = "⚠️ Không thể xử lý yêu cầu.";
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: aiResponseText,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error("Lỗi khi gửi tin nhắn:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "❌ Không thể kết nối đến máy chủ. Vui lòng thử lại.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col bg-gradient-to-b from-blue-50/30 via-purple-50/20 to-white">
      {/* Chat Container - Khu vực tin nhắn có thể cuộn */}
      <div 
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto pb-4"
      >
        {messages.length === 0 ? (
          <WelcomeScreen onPromptClick={handleSendMessage} />
        ) : (
          <div className="max-w-4xl mx-auto px-4 py-8">
            {messages.map(message => (
              <ChatMessage 
                key={message.id} 
                message={message.text} 
                isUser={message.isUser} 
                timestamp={message.timestamp}
                images={message.images}
              />
            ))}

            {isTyping && (
              <div className="flex justify-start mb-6">
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-3">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  </div>
                  <div className="bg-gray-100 px-5 py-3 rounded-3xl rounded-tl-md">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{
                        animationDelay: '0ms'
                      }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{
                        animationDelay: '150ms'
                      }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{
                        animationDelay: '300ms'
                      }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Ô nhập liệu cố định ở dưới cùng */}
      <div className="flex-shrink-0 bg-gradient-to-t from-white via-white to-transparent pt-4">
        <div className="max-w-4xl mx-auto px-4">
          <ChatInput onSend={handleSendMessage} disabled={isTyping} />
        </div>
      </div>
    </div>
  );
}