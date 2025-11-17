// src/components/ui/ConfirmDialog.tsx
import React from 'react';
import { AlertTriangleIcon, XIcon } from 'lucide-react';

interface ConfirmDialogProps {
  isOpen: boolean;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

export const ConfirmDialog: React.FC<ConfirmDialogProps> = ({ isOpen, message, onConfirm, onCancel }) => {
  // Ngăn người dùng scroll trang nền khi modal mở
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    // Dọn dẹp khi component bị hủy
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    // Lớp nền mờ
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      {/* Nội dung modal */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 m-4 max-w-sm w-full transform transition-all">
        {/* Tiêu đề và icon */}
        <div className="flex items-center mb-4">
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
            <AlertTriangleIcon className="w-6 h-6 text-red-600 dark:text-red-400" />
          </div>
          <h3 className="ml-3 text-lg font-semibold text-gray-900 dark:text-white">Xác nhận xóa</h3>
          <button onClick={onCancel} className="ml-auto text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <XIcon className="w-6 h-6" />
          </button>
        </div>

        {/* Nội dung thông báo */}
        <p className="text-gray-600 dark:text-gray-400 mb-6">{message}</p>

        {/* Các nút hành động */}
        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
          >
            Hủy
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors"
          >
            Xóa
          </button>
        </div>
      </div>
    </div>
  );
};