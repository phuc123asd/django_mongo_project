import React, { useState, useEffect } from 'react';
import { XIcon, BotIcon, UserIcon, SaveIcon, TrashIcon } from 'lucide-react';
import { Button } from '../ui/Button';

// Interface cho response từ API
interface AdminResponseData {
  id: string;
  review_id: string;
  response: string;
  admin_id: string;
  admin_name: string;
  created_at: string;
  updated_at: string;
  response_type: 'manual' | 'ai';
}

interface AdminResponseModalProps {
  isOpen: boolean;
  onClose: () => void;
  reviewId: string;
  reviewRating: number;
  reviewComment: string;
  productName: string;
}

export const AdminResponseModal: React.FC<AdminResponseModalProps> = ({
  isOpen,
  onClose,
  reviewId,
  reviewRating,
  reviewComment,
  productName
}) => {
  const [responses, setResponses] = useState<AdminResponseData[]>([]);
  const [newResponse, setNewResponse] = useState('');
  const [editingResponse, setEditingResponse] = useState<string | null>(null);
  const [editText, setEditText] = useState('');
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error';
    message: string;
    show: boolean;
  }>({ type: 'success', message: '', show: false });

  // Fetch responses khi modal mở
  useEffect(() => {
    if (isOpen && reviewId) {
      fetchResponses();
    }
  }, [isOpen, reviewId]);

  const fetchResponses = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/admin-responses/${reviewId}/`);
      if (response.ok) {
        const data = await response.json();
        setResponses(data);
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error fetching admin responses:', error);
      showNotification('error', 'Không thể tải phản hồi');
    } finally {
      setLoading(false);
    }
  };

  const showNotification = (type: 'success' | 'error', message: string) => {
    setNotification({ type, message, show: true });
    setTimeout(() => {
      setNotification(prev => ({ ...prev, show: false }));
    }, 3000);
  };

  const handleAddResponse = async () => {
    if (!newResponse.trim()) {
      showNotification('error', 'Vui lòng nhập nội dung phản hồi');
      return;
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/admin-responses/add/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          review_id: reviewId,
          response: newResponse.trim(),
        }),
      });

      if (response.ok) {
        setNewResponse('');
        fetchResponses(); // Tải lại danh sách
        showNotification('success', 'Đã thêm phản hồi thành công');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error adding admin response:', error);
      showNotification('error', 'Không thể thêm phản hồi');
    }
  };

  const handleGenerateAIResponse = async () => {
    setGenerating(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/admin-responses/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          review_id: reviewId,
          rating: reviewRating,
          comment: reviewComment,
          product_name: productName,
        }),
      });

      if (response.ok) {
        fetchResponses(); // Tải lại danh sách
        showNotification('success', 'Đã tạo phản hồi AI thành công');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error generating AI response:', error);
      showNotification('error', 'Không thể tạo phản hồi AI');
    } finally {
      setGenerating(false);
    }
  };

  const handleUpdateResponse = async (responseId: string) => {
    if (!editText.trim()) {
      showNotification('error', 'Vui lòng nhập nội dung phản hồi');
      return;
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/admin-responses/update/${responseId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          response: editText.trim(),
        }),
      });

      if (response.ok) {
        setEditingResponse(null);
        fetchResponses(); // Tải lại danh sách
        showNotification('success', 'Đã cập nhật phản hồi thành công');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error updating admin response:', error);
      showNotification('error', 'Không thể cập nhật phản hồi');
    }
  };

  const handleDeleteResponse = async (responseId: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa phản hồi này?')) {
      return;
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/admin-responses/delete/${responseId}/`, {
        method: 'DELETE',
      });

      if (response.ok) {
        fetchResponses(); // Tải lại danh sách
        showNotification('success', 'Đã xóa phản hồi thành công');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting admin response:', error);
      showNotification('error', 'Không thể xóa phản hồi');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Quản lý phản hồi</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <XIcon className="w-6 h-6" />
          </button>
        </div>

        {/* Notification */}
        {notification.show && (
          <div className={`mx-6 mt-4 p-3 rounded-lg flex items-center gap-2 ${
            notification.type === 'success' 
              ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400' 
              : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
          }`}>
            {notification.type === 'success' ? (
              <SaveIcon className="w-5 h-5" />
            ) : (
              <XIcon className="w-5 h-5" />
            )}
            <span>{notification.message}</span>
          </div>
        )}

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Review Info */}
          <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <h3 className="font-medium text-gray-900 dark:text-white mb-2">Đánh giá của khách hàng</h3>
            <div className="flex items-center gap-2 mb-2">
              {[...Array(5)].map((_, i) => (
                <svg key={i} className={`w-4 h-4 ${i < reviewRating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
              <span className="text-sm text-gray-600 dark:text-gray-400">({reviewRating} sao)</span>
            </div>
            <p className="text-gray-700 dark:text-gray-300">{reviewComment}</p>
          </div>

          {/* Existing Responses */}
          <div className="mb-6">
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Phản hồi đã có</h3>
            {loading ? (
              <div className="flex justify-center py-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
              </div>
            ) : responses.length === 0 ? (
              <p className="text-gray-500 dark:text-gray-400 italic">Chưa có phản hồi nào</p>
            ) : (
              <div className="space-y-3">
                {responses.map((response) => (
                  <div key={response.id} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {response.response_type === 'ai' ? (
                          <BotIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                        ) : (
                          <UserIcon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                        )}
                        <span className="font-medium text-gray-900 dark:text-white">{response.admin_name}</span>
                        <span className="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
                          {response.response_type === 'ai' ? 'AI' : 'Admin'}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {new Date(response.created_at).toLocaleString()}
                      </span>
                    </div>
                    
                    {editingResponse === response.id ? (
                      <div>
                        <textarea
                          value={editText}
                          onChange={(e) => setEditText(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white mb-3"
                          rows={4}
                        />
                        <div className="flex gap-2">
                          <Button
                            onClick={() => handleUpdateResponse(response.id)}
                            className="flex items-center gap-1"
                          >
                            <SaveIcon className="w-4 h-4" />
                            Lưu
                          </Button>
                          <Button
                            variant="outline"
                            onClick={() => setEditingResponse(null)}
                          >
                            Hủy
                          </Button>
                        </div>
                      </div>
                    ) : (
                      <div>
                        <p className="text-gray-700 dark:text-gray-300 mb-3 whitespace-pre-line">
                          {response.response}
                        </p>
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setEditingResponse(response.id);
                              setEditText(response.response);
                            }}
                          >
                            Chỉnh sửa
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleDeleteResponse(response.id)}
                            className="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                          >
                            <TrashIcon className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Add New Response */}
          <div>
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Thêm phản hồi mới</h3>
            <textarea
              value={newResponse}
              onChange={(e) => setNewResponse(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white mb-3"
              rows={4}
              placeholder="Nhập nội dung phản hồi..."
            />
            <div className="flex gap-2">
              <Button onClick={handleAddResponse} disabled={!newResponse.trim()}>
                Gửi phản hồi
              </Button>
              <Button
                variant="outline"
                onClick={handleGenerateAIResponse}
                disabled={generating}
                className="flex items-center gap-1"
              >
                {generating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b border-indigo-600"></div>
                    Đang tạo...
                  </>
                ) : (
                  <>
                    <BotIcon className="w-4 h-4" />
                    Tạo bằng AI
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200 dark:border-gray-700">
          <Button variant="outline" onClick={onClose}>
            Đóng
          </Button>
        </div>
      </div>
    </div>
  );
};