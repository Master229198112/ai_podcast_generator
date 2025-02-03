import React from "react";

export const Button = ({ children, onClick, className }) => {
  return (
    <button 
      className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 ${className}`} 
      onClick={onClick}
    >
      {children}
    </button>
  );
};