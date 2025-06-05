// Projekt: gallery.kado-ber.de
// Ziel: Galerie für Stable-Diffusion-Bilder mit Kategorie- und Tag-Filterung

import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles/globals.css";

interface ImageData {
  src: string;
  alt: string;
  category: string;
  tags: string[];
}

const IMAGES_PER_PAGE = 12;

function Lightbox({
  image,
  onClose,
  onPrev,
  onNext,
}: {
  image: ImageData;
  onClose: () => void;
  onPrev: () => void;
  onNext: () => void;
}) {
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowLeft") onPrev();
      if (e.key === "ArrowRight") onNext();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onClose, onPrev, onNext]);

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-90 flex flex-col items-center justify-center z-50 transition-opacity duration-300 animate-fade-in px-4"
      onClick={onClose}
    >
      <div className="relative w-full max-w-5xl">
        <img
          src={image.src}
          alt={image.alt}
          className="mx-auto max-w-full max-h-[80vh] shadow-2xl rounded-md"
          onClick={(e) => e.stopPropagation()}
        />

        <button
          onClick={(e) => {
            e.stopPropagation();
            onClose();
          }}
          className="absolute top-4 right-6 text-white text-3xl font-bold hover:text-purple-400"
        >
          &times;
        </button>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onPrev();
          }}
          className="absolute left-0 top-1/2 -translate-y-1/2 bg-gray-800 bg-opacity-70 hover:bg-opacity-100 text-white text-3xl px-3 py-1 rounded"
        >
          &#8592;
        </button>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onNext();
          }}
          className="absolute right-0 top-1/2 -translate-y-1/2 bg-gray-800 bg-opacity-70 hover:bg-opacity-100 text-white text-3xl px-3 py-1 rounded"
        >
          &#8594;
        </button>
      </div>

      <div className="mt-4 text-center text-sm text-gray-300 max-w-xl">
        <p className="mb-2 italic">„{image.alt}“</p>
        <a
          href={`mailto:kai.dombrowski@web.de?subject=Bildanfrage: ${encodeURIComponent(
            image.alt
          )} (${encodeURIComponent(image.src.split("/").pop()!)})`}
          onClick={(e) => e.stopPropagation()}
          className="inline-block mt-1 px-4 py-1 rounded bg-purple-600 hover:bg-purple-700 text-white text-sm"
        >
          📩 Dieses Bild anfragen
        </a>
      </div>
    </div>
  );
}

function App() {
  const [images, setImages] = useState<ImageData[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [activeCategory, setActiveCategory] = useState<string>("Alle");
  const [activeTag, setActiveTag] = useState<string | null>(null);

  useEffect(() => {
    fetch("/data/images.json")
      .then((res) => res.json())
      .then((data) => setImages(data))
      .catch((err) => console.error("Fehler beim Laden der Bilder:", err));
  }, []);

  const allCategories = [
    "Alle",
    ...Array.from(new Set(images.map((img) => img.category))),
  ];
  const allTags = Array.from(new Set(images.flatMap((img) => img.tags)));

  const filteredImages = images.filter((img) => {
    const categoryMatch =
      activeCategory === "Alle" || img.category === activeCategory;
    const tagMatch = !activeTag || img.tags.includes(activeTag);
    return categoryMatch && tagMatch;
  });

  const selectedImage =
    selectedIndex !== null ? filteredImages[selectedIndex] : null;

  const startIdx = (currentPage - 1) * IMAGES_PER_PAGE;
  const endIdx = startIdx + IMAGES_PER_PAGE;
  const paginatedImages = filteredImages.slice(startIdx, endIdx);
  const totalPages = Math.ceil(filteredImages.length / IMAGES_PER_PAGE);

  const handlePrev = () => {
    if (selectedIndex !== null) {
      setSelectedIndex((prev) =>
        prev! > 0 ? prev! - 1 : filteredImages.length - 1
      );
    }
  };

  const handleNext = () => {
    if (selectedIndex !== null) {
      setSelectedIndex((prev) =>
        prev! < filteredImages.length - 1 ? prev! + 1 : 0
      );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a40] to-[#2d0068] text-white font-sans">
      <header className="w-full py-6 px-8 bg-[#0f0f1a] shadow-md">
        <h1 className="text-2xl font-bold text-purple-400">
          gallery.kado-ber.de
        </h1>
      </header>

      <main className="p-8">
        <h2 className="text-3xl font-semibold mb-6">Galerieansicht</h2>

        {/* Filter UI */}
        <div className="flex flex-wrap items-center gap-4 mb-6">
          <select
            value={activeCategory}
            onChange={(e) => {
              setActiveCategory(e.target.value);
              setCurrentPage(1);
            }}
            className="bg-gray-800 text-white px-4 py-2 rounded shadow"
          >
            {allCategories.map((cat, idx) => (
              <option key={idx} value={cat}>
                {cat}
              </option>
            ))}
          </select>

          <div className="flex flex-wrap gap-2">
            {allTags.map((tag, idx) => (
              <button
                key={idx}
                onClick={() => setActiveTag(tag === activeTag ? null : tag)}
                className={`px-3 py-1 rounded-full text-sm border ${
                  tag === activeTag
                    ? "bg-purple-600 border-purple-300"
                    : "bg-gray-700 border-gray-500"
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>

        {/* Bild-Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {paginatedImages.map((img, index) => (
            <div
              key={startIdx + index}
              className="overflow-hidden rounded-xl shadow-md hover:scale-[1.02] transition-transform cursor-pointer"
              onClick={() => setSelectedIndex(startIdx + index)}
            >
              <img
                src={img.src}
                alt={img.alt}
                className="w-full object-cover"
              />
            </div>
          ))}
        </div>

        {/* Pagination */}
        <div className="flex justify-center mt-8 space-x-4">
          <button
            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 rounded bg-gray-700 hover:bg-gray-600 disabled:opacity-30"
          >
            Zurück
          </button>
          <span className="self-center text-sm text-gray-300">
            Seite {currentPage} von {totalPages}
          </span>
          <button
            onClick={() =>
              setCurrentPage((prev) => Math.min(prev + 1, totalPages))
            }
            disabled={currentPage === totalPages}
            className="px-4 py-2 rounded bg-gray-700 hover:bg-gray-600 disabled:opacity-30"
          >
            Weiter
          </button>
        </div>
      </main>

      <footer className="mt-auto bg-[#0f0f1a] py-4 px-8 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Kai Dombrowski – Alle Rechte
        vorbehalten.
      </footer>

      {selectedImage && (
        <Lightbox
          image={selectedImage}
          onClose={() => setSelectedIndex(null)}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      )}
    </div>
  );
}

const container = document.getElementById("root");
const root = createRoot(container!);
root.render(<App />);

// TailwindCSS animation (optional: in globals.css oder tailwind.config hinzufügen)
// @keyframes fade-in {
//   from { opacity: 0; }
//   to { opacity: 1; }
// }
// .animate-fade-in {
//   animation: fade-in 0.3s ease-out;
// }
