import { useState, useRef, useEffect } from 'react';
import { MessageCircleIcon, XIcon, SendIcon, BotIcon, UserIcon, CopyIcon, RotateCcwIcon } from 'lucide-react';

// --- Interfaces ---
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  isError?: boolean; // Thêm cờ để nhận diện tin nhắn lỗi
}

interface QuickAction {
  label: string;
  query: string;
}

// --- Constants ---
const initialBotMessage: Message = {
  id: 1,
  text: 'Xin chào! Tôi là trợ lý tư vấn của TechHub. Tôi có thể giúp gì cho bạn hôm nay? Bạn có thể hỏi về sản phẩm, giao hàng, đổi trả, bảo hành, thanh toán hoặc bất kỳ thắc mắc nào!',
  sender: 'bot',
  timestamp: new Date(),
};

const quickActions: QuickAction[] = [
  { label: '📦 Thông tin giao hàng', query: 'Cho tôi biết về chính sách giao hàng' },
  { label: '↩️ Chính sách đổi trả', query: 'Chính sách đổi trả như thế nào?' },
  { label: '🛡️ Bảo hành', query: 'Sản phẩm được bảo hành bao lâu?' },
  { label: '💳 Thanh toán', query: 'Các hình thức thanh toán' },
  { label: '📱 Tư vấn sản phẩm', query: 'Tôi muốn tư vấn về điện thoại' },
  { label: '💰 Khuyến mãi', query: 'Có khuyến mãi gì không?' }
];

// --- Sub-components ---

// Header của cửa sổ chat
const ChatHeader = ({ onClear, onClose }: { onClear: () => void, onClose: () => void }) => (
  <div className="bg-indigo-600 text-white rounded-t-lg p-4 flex items-center justify-between">
    <div className="flex items-center gap-2">
      <div className="relative">
        <BotIcon className="w-6 h-6" />
        <span className="absolute bottom-0 right-0 w-2 h-2 bg-green-400 rounded-full border border-white"></span>
      </div>
      <div>
        <h3 className="font-semibold">TechHub Assistant</h3>
        <p className="text-xs text-indigo-100">Online • Phản hồi nhanh chóng</p>
      </div>
    </div>
    <div className="flex gap-2">
      <button onClick={onClear} className="hover:bg-indigo-700 rounded-full p-1 text-xs" title="Xóa lịch sử">
        Xóa
      </button>
      <button onClick={onClose} className="hover:bg-indigo-700 rounded-full p-1">
        <XIcon className="w-5 h-5" />
      </button>
    </div>
  </div>
);

// Bong bóng chat cho mỗi tin nhắn
const MessageBubble = ({ message, onRetry, onCopy }: { 
  message: Message, 
  onRetry?: () => void, 
  onCopy?: () => void 
}) => {
  const isUser = message.sender === 'user';
  const isError = message.isError;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] rounded-lg p-3 group relative ${
        isUser
          ? 'bg-indigo-600 text-white'
          : isError 
            ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-300 dark:border-red-700'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
      }`}>
        <div className="flex items-start gap-2">
          {!isUser && <BotIcon className="w-5 h-5 mt-0.5 flex-shrink-0" />}
          <div className="flex-1">
            <p className="text-sm whitespace-pre-wrap">{message.text}</p>
            <p className={`text-xs mt-1 ${isUser ? 'text-indigo-100' : 'text-gray-500 dark:text-gray-400'}`}>
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
          {isUser && <UserIcon className="w-5 h-5 mt-0.5 flex-shrink-0" />}
        </div>
        
        {/* Các nút hành động chỉ hiện khi hover */}
        {!isUser && (
          <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
            {onCopy && (
              <button onClick={onCopy} className="p-1 bg-white dark:bg-gray-600 rounded shadow-md text-gray-700 dark:text-gray-200" title="Sao chép">
                <CopyIcon className="w-3 h-3" />
              </button>
            )}
            {isError && onRetry && (
              <button onClick={onRetry} className="p-1 bg-white dark:bg-gray-600 rounded shadow-md text-red-600 dark:text-red-400" title="Thử lại">
                <RotateCcwIcon className="w-3 h-3" />
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// Component các hành động nhanh
const QuickActionsComponent = ({ actions, onActionClick }: { actions: QuickAction[], onActionClick: (query: string) => void }) => (
  <div className="space-y-2">
    <p className="text-xs text-gray-500 dark:text-gray-400 text-center">Câu hỏi nhanh:</p>
    <div className="grid grid-cols-2 gap-2">
      {actions.map((action) => (
        <button
          key={action.query}
          onClick={() => onActionClick(action.query)}
          className="text-xs bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 hover:bg-indigo-50 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg px-3 py-2 transition-colors"
        >
          {action.label}
        </button>
      ))}
    </div>
  </div>
);

// Component nhập liệu
const ChatInput = ({ input, setInput, onSend, isTyping }: { 
  input: string, 
  setInput: (val: string) => void, 
  onSend: () => void, 
  isTyping: boolean 
}) => (
  <form onSubmit={(e) => { e.preventDefault(); onSend(); }} className="p-4 border-t border-gray-200 dark:border-gray-700">
    <div className="flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Nhập tin nhắn của bạn..."
        className="flex-grow px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        disabled={isTyping}
      />
      <button
        type="submit"
        className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 transition-colors disabled:opacity-50"
        disabled={!input.trim() || isTyping}
      >
        <SendIcon className="w-5 h-5" />
      </button>
    </div>
  </form>
);


// --- Main Component ---
export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>(() => {
    const savedMessages = localStorage.getItem('chatMessages');
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        return parsed.map((msg: any) => ({ ...msg, timestamp: new Date(msg.timestamp) }));
      } catch (e) {
        console.error('Failed to parse saved messages:', e);
        return [initialBotMessage];
      }
    }
    return [initialBotMessage];
  });
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const lastFailedMessageRef = useRef<string | null>(null);

  useEffect(() => {
    if (messages.length > 1) {
      localStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || isTyping) return;
    lastFailedMessageRef.current = null; // Reset failed message on new send

    const userMessage: Message = {
      id: Date.now(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      // !!! QUAN TRỌNG: Vẫn cần cấu hình CORS trên server backend !!!
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chatbot/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text.trim() }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      const botMessage: Message = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      lastFailedMessageRef.current = text.trim(); // Lưu lại tin nhắn bị lỗi để thử lại
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Xin lỗi, đã có lỗi xảy ra khi kết nối với trợ lý AI. Vui lòng thử lại sau.',
        sender: 'bot',
        timestamp: new Date(),
        isError: true, // Đánh dấu là lỗi
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleRetry = () => {
    if (lastFailedMessageRef.current) {
      // Xóa tin nhắn lỗi cuối cùng trước khi thử lại
      setMessages(prev => prev.slice(0, -1));
      sendMessage(lastFailedMessageRef.current);
    }
  };
  
  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    // Có thể thêm thông báo "Đã sao chép!" ở đây
  };

  const clearChat = () => { // <<<< DÒNG ĐÃ ĐƯỢC SỬA
    if (window.confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử trò chuyện?')) {
      setMessages([initialBotMessage]);
      localStorage.removeItem('chatMessages');
    }
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full p-4 shadow-lg transition-all hover:scale-110 animate-pulse"
          aria-label="Open chat"
        >
          <MessageCircleIcon className="w-6 h-6" />
          {messages.length > 1 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {Math.min(messages.length - 1, 9)}
            </span>
          )}
        </button>
      )}

      {isOpen && (
        // CẢI TIẾN: Tối ưu responsive, full width trên mobile
        <div className="fixed bottom-0 right-0 z-50 w-full h-full sm:w-96 sm:h-[600px] sm:bottom-6 sm:right-6 bg-white dark:bg-gray-800 rounded-lg sm:rounded-lg shadow-2xl flex flex-col">
          
          <ChatHeader onClear={clearChat} onClose={() => setIsOpen(false)} />

          <div className="flex-grow overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <MessageBubble
                key={message.id}
                message={message}
                onRetry={message.isError ? handleRetry : undefined}
                onCopy={() => handleCopy(message.text)}
              />
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3">
                  <div className="flex items-center gap-2">
                    <BotIcon className="w-5 h-5" />
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {messages.length <= 2 && <QuickActionsComponent actions={quickActions} onActionClick={sendMessage} />}
            
            <div ref={messagesEndRef} />
          </div>

          <ChatInput 
            input={inputMessage} 
            setInput={setInputMessage} 
            onSend={() => sendMessage(inputMessage)} 
            isTyping={isTyping} 
          />
        </div>
      )}
    </>
  );
};