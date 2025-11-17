import { useState } from 'react';
import { Avatar } from './ui/Avatar';
import { CopyIcon, CheckIcon, SparklesIcon } from 'lucide-react';
import { formatTime } from '../utils/formatters';

export interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: Date;
  images?: string[]; // Thêm prop để hỗ trợ hiển thị ảnh
}

export function ChatMessage({
  message,
  isUser,
  timestamp,
  images
}: ChatMessageProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Component con để hiển thị ảnh preview trong tin nhắn
  const ImagePreview = ({ previewImages }: { previewImages: string[] }) => (
    <div className="flex flex-wrap gap-2 mt-2 p-2 border border-gray-200 rounded-xl bg-gray-50">
      {previewImages.map((preview, index) => (
        <div key={index} className="relative group">
          <img 
            src={preview} 
            alt={`Image ${index + 1}`} 
            className="h-24 w-24 object-cover rounded-lg"
          />
          {/* Có thể thêm nút remove nếu cần, nhưng vì đã gửi nên chỉ hiển thị */}
        </div>
      ))}
    </div>
  );

  if (isUser) {
    return (
      <div className="flex justify-end mb-6 animate-fadeIn">
        <div className="flex flex-row-reverse items-start max-w-[80%] md:max-w-[70%]">
          <div className="ml-3 flex-shrink-0">
            <Avatar fallback="A" size="sm" />
          </div>
          <div className="space-y-1">
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-5 py-3 rounded-3xl rounded-tr-md shadow-sm">
              <p className="text-[15px] leading-relaxed">{message}</p>
              {/* Hiển thị ảnh nếu có, bên dưới văn bản */}
              {images && images.length > 0 && <ImagePreview previewImages={images} />}
            </div>
            <p className="text-xs text-gray-500 text-right px-2">
              {formatTime(timestamp)}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start mb-6 animate-fadeIn">
      <div className="flex items-start max-w-[80%] md:max-w-[70%]">
        <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-3">
          <SparklesIcon className="w-4 h-4 text-white" />
        </div>
        <div className="space-y-1 flex-1">
          <div className="bg-gray-100 px-5 py-3 rounded-3xl rounded-tl-md">
            <p className="text-[15px] leading-relaxed text-gray-900">
              {message}
            </p>
            {/* Hiển thị ảnh nếu có, bên dưới văn bản */}
            {images && images.length > 0 && <ImagePreview previewImages={images} />}
          </div>
          <div className="flex items-center justify-between px-2">
            <p className="text-xs text-gray-500">{formatTime(timestamp)}</p>
            <button 
              onClick={handleCopy} 
              className="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded hover:bg-gray-200" 
              title="Copy message"
            >
              {copied ? <CheckIcon className="w-4 h-4 text-green-600" /> : <CopyIcon className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}