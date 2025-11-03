import React, { CSSProperties, MouseEvent, ReactNode, useState } from "react";
import { getSize } from "../../utils/functions";

interface TooltipProps {
  children: ReactNode;
  content: string | ReactNode;
  position?: "left" | "right";
  color?: string;
}

interface TooltipPosition {
  top: number;
  left: number;
}

const Tooltip: React.FC<TooltipProps> = ({ children, content, position = "right", color }) => {
  const [show, setShow] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ top: 0, left: 0 });

  const tooltipOffset = 10;

  const handleMouseEnter = () => setShow(true);

  const handleMouseLeave = () => setShow(false);

  const handleMouseMove = (event: MouseEvent<HTMLDivElement>) => {
    const tooltipPosition: TooltipPosition = { top: 0, left: 0 };
    switch (position) {
      case "left":
        tooltipPosition.top = event.clientY + tooltipOffset;
        tooltipPosition.left = event.clientX - getSize().width - tooltipOffset;
        break;
      case "right":
      default:
        tooltipPosition.top = event.clientY + tooltipOffset;
        tooltipPosition.left = event.clientX + tooltipOffset;
        break;
    }
    setTooltipPosition(tooltipPosition);
  };

  const tooltipStyle: CSSProperties = {
    position: "fixed",
    top: tooltipPosition.top + "px",
    left: tooltipPosition.left + "px",
    zIndex: 10,
    color: color,
    fontSize: "0.8rem",
    padding: "0px 8px 0px 8px",
  };

  return (
    <div
      id='tooltip'
      className='relative'
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onMouseMove={handleMouseMove}
    >
      {show && <div style={tooltipStyle}>{content}</div>}
      {children}
    </div>
  );
};

export default Tooltip;
