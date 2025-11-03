import React, { ReactNode, MouseEvent, CSSProperties, ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  label?: string;
  children?: ReactNode;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
  style?: CSSProperties;
  onClick?: (event: MouseEvent<HTMLButtonElement>) => void;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({ label, children, disabled, type, style, onClick, className }) => {
  return (
    <button
      disabled={disabled}
      type={type}
      style={style}
      onClick={onClick}
      className={`${disabled ? "py-1 px-2 rounded opacity-50" : "hover:opacity-80 py-1 px-2 rounded"} ${className}`}
    >
      {children && children}
      {label && label}
    </button>
  );
};

export default Button;
