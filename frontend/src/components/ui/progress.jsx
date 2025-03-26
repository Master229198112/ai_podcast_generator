import React from "react";

export const Progress = ({ value, max }) => {
  return (
    <progress 
      className="w-full h-2 rounded bg-gray-300" 
      value={value} 
      max={max}
    >
      {value}%
    </progress>
  );
};