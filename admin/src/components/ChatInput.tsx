import React, { useEffect, useState, useRef } from 'react';
import { SendIcon, SparklesIcon, ImageIcon, X } from 'lucide-react';

export interface ChatInputProps {
  onSend: (message: string, images?: File[]) => void;
  disabled?: boolean;
}

export function ChatInput({
  onSend,
  disabled = false
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [selectedImages, setSelectedImages] = useState<File[]>([]);
  const [previewImages, setPreviewImages] = useState<string[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if ((message.trim() || selectedImages.length > 0) && !disabled) {
      onSend(message.trim(), selectedImages);
      setMessage('');
      setSelectedImages([]);
      setPreviewImages([]);
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    
    // Filter for image files only
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (imageFiles.length > 0) {
      setSelectedImages(prev => [...prev, ...imageFiles]);
      
      // Create preview URLs
      imageFiles.forEach(file => {
        const reader = new FileReader();
        reader.onload = (event) => {
          if (event.target?.result) {
            setPreviewImages(prev => [...prev, event.target.result as string]);
          }
        };
        reader.readAsDataURL(file);
      });
    }
    
    // Reset the input value to allow selecting the same file again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeImage = (index: number) => {
    setSelectedImages(prev => prev.filter((_, i) => i !== index));
    setPreviewImages(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative bg-white rounded-3xl shadow-lg border border-gray-200 focus-within:border-blue-500 focus-within:shadow-xl transition-all duration-200">
          {/* Image previews */}
          {previewImages.length > 0 && (
            <div className="flex flex-wrap gap-2 p-3 pt-4 border-b border-gray-100">
              {previewImages.map((preview, index) => (
                <div key={index} className="relative group">
                  <img 
                    src={preview} 
                    alt={`Preview ${index}`} 
                    className="h-20 w-20 object-cover rounded-lg border border-gray-200"
                  />
                  <button
                    type="button"
                    onClick={() => removeImage(index)}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          )}
          
          <div className="flex items-end p-2">
            <div className="flex-shrink-0 p-3">
              <SparklesIcon className="w-5 h-5 text-gray-400" />
            </div>
            
            <textarea 
              ref={textareaRef} 
              value={message} 
              onChange={e => setMessage(e.target.value)} 
              placeholder="Ask me anything about your store..." 
              disabled={disabled} 
              rows={1} 
              className="flex-1 px-2 py-3 bg-transparent focus:outline-none resize-none text-[15px] text-gray-900 placeholder-gray-400 max-h-32" 
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }} 
            />
            
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageUpload}
              className="hidden"
            />
            
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled}
              className="flex-shrink-0 m-2 p-3 text-gray-400 hover:text-blue-600 rounded-full hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              title="Upload images"
            >
              <ImageIcon className="w-5 h-5" />
            </button>
            
            <button 
              type="submit" 
              disabled={(!message.trim() && selectedImages.length === 0) || disabled} 
              className="flex-shrink-0 m-2 p-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-full hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-md disabled:hover:shadow-none"
            >
              <SendIcon className="w-5 h-5" />
            </button>
          </div>
        </div>
      </form>

      <p className="text-xs text-gray-500 text-center mt-3">
        TechStore AI can make mistakes. Consider checking important information.
      </p>
    </div>
  );
}