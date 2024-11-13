import React from "react";

interface SpinnerProps {
  className?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({ className = "" }) => {
  return (
    <div className={`relative ${className}`}>
      <div
        className="w-4 h-4 rounded-full absolute
                      border-2 border-solid border-gray-200"
      ></div>
      <div
        className="w-4 h-4 rounded-full animate-spin absolute
                      border-2 border-solid border-white border-t-transparent"
      ></div>
    </div>
  );
};
