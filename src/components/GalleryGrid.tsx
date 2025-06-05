import React from "react";
import { ImageCard } from "./ImageCard";

// Beispielbilder – du kannst das mit echten Pfaden ersetzen
const images = [
  {
    src: "/images/StockMuse_Office_00004_.png",
    alt: "Bild 1",
    caption: "Modern Office",
  },
  {
    src: "/images/StockMuse_Nutrition_00003_.png",
    alt: "Bild 2",
    caption: "Healthy Lifestyle",
  },
  {
    src: "/images/StockMuse_AI_00010_.png",
    alt: "Bild 3",
    caption: "AI & Innovation",
  },
];

export const GalleryGrid: React.FC = () => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {images.map((img, index) => (
        <ImageCard key={index} {...img} />
      ))}
    </div>
  );
};
