import React, { memo } from "react";
import { Page } from "react-pdf";

const PdfPage = ({
  key,
  zoom,
  index,
  style,
  height,
  observePage,
  visiblePages,
  elWidth,
}) => {
  return (
    <div
      key={`wrapper_${index}`}
      style={{ height }}
      data-page-number={index}
      ref={(node) => observePage(node, index)}
    >
      <Page
        loading=''
        className='mb-8 border border-gray-300 shadow-xl'
        id='page'
        key={`page_${index + 1}`}
        size='A4'
        style={style}
        pageNumber={index + 1} // It should render all pages, not just the current page
        scale={zoom}
        renderMode='canvas'
        renderTextLayer={false}
        width={elWidth}
      />
    </div>
  );
};

export default memo(PdfPage);
