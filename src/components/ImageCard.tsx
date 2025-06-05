import React from "react";

interface ImageCardProps {
  src: string;
  alt: string;
  caption?: string;
}

export const ImageCard: React.FC<ImageCardProps> = ({ src, alt, caption }) => {
  return (
    <div className="overflow-hidden rounded-xl shadow-md hover:scale-[1.02] transition-transform">
      <img src={src} alt={alt} className="w-full object-cover" />
      {caption && (
        <div className="p-2 text-sm text-gray-300 bg-black bg-opacity-50">
          {caption}
        </div>
      )}
    </div>
  );
};
