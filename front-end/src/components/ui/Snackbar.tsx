import React, { useState, useEffect, FC } from "react";
import { light_secondary } from "../../utils/consts";

interface Props {
  message: string;
  status: "success" | "error" | "info";
  duration?: number;
  onClose?: () => void;
}

const Snackbar: FC<Props> = ({ message, status, duration = 2000, onClose }) => {
  const [visible, setVisible] = useState<boolean>(!!message);

  useEffect(() => {
    if (message && visible) {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose && onClose();
      }, duration);
      return () => {
        clearTimeout(timer);
      };
    }
  }, [message, visible, duration, onClose, setVisible]);

  const getStatusStyle = (status: "success" | "error" | "info"): string => {
    switch (status) {
      case "success":
        return "bg-green-600";
      case "error":
        return "bg-red-600";
      case "info":
        return "bg-blue-600";
      default:
        return "bg-gray-400";
    }
  };

  if (!visible) return null;

  return (
    <div
      className={`fixed bottom-16 left-[1.3rem] p-2 rounded shadow-lg ${getStatusStyle(status)} z-50`}
      style={{ color: light_secondary }}
    >
      {message}
    </div>
  );
};

export default Snackbar;
