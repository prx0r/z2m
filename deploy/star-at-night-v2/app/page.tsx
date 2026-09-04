'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { create } from 'zustand';

interface Photo {
  id: string;
  file: File;
  preview: string;
}

interface Product {
  id: string;
  type: string;
  title: string;
  subtitle: string;
  badge: string;
  photoIds: string[];
  madeFrom: string;
}

interface Store {
  photos: Photo[];
  products: Product[];
  stage: 'upload' | 'generating' | 'results';
  addPhotos: (files: File[]) => void;
  setStage: (stage: 'upload' | 'generating' | 'results') => void;
  setProducts: (products: Product[]) => void;
}

const useStore = create<Store>((set) => ({
  photos: [],
  products: [],
  stage: 'upload',
  addPhotos: (files) =>
    set((state) => ({
      photos: [
        ...state.photos,
        ...files.map((file) => ({
          id: crypto.randomUUID(),
          file,
          preview: URL.createObjectURL(file),
        })),
      ],
    })),
  setStage: (stage) => set({ stage }),
  setProducts: (products) => set({ products }),
}));

export default function Home() {
  const { photos, products, stage, addPhotos, setStage, setProducts } = useStore();

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      addPhotos(acceptedFiles);
    },
    [addPhotos]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.heic', '.webp'] },
    multiple: true,
  });

  const generateProducts = async () => {
    setStage('generating');
    
    // Simulate AI generation
    await new Promise((r) => setTimeout(r, 3000));
    
    const mockProducts: Product[] = [
      {
        id: '1',
        type: 'newspaper',
        title: 'The Times',
        subtitle: 'A very special edition',
        badge: 'NEWSPAPER',
        photoIds: photos.map((p) => p.id),
        madeFrom: photos.map((p) => p.file.name.split('.')[0]).join(' · '),
      },
      {
        id: '2',
        type: 'book',
        title: 'The Biography',
        subtitle: 'An unauthorized account of a life well-lived',
        badge: 'BOOK',
        photoIds: photos.map((p) => p.id),
        madeFrom: photos.map((p) => p.file.name.split('.')[0]).join(' · '),
      },
      {
        id: '3',
        type: 'ornament',
        title: 'Christmas Ornament',
        subtitle: 'A keepsake for years to come',
        badge: 'ORNAMENT',
        photoIds: photos.map((p) => p.id),
        madeFrom: photos.map((p) => p.file.name.split('.')[0]).join(' · '),
      },
      {
        id: '4',
        type: 'puzzle',
        title: 'Custom Puzzle',
        subtitle: '500 pieces of memories',
        badge: 'PUZZLE',
        photoIds: photos.map((p) => p.id),
        madeFrom: photos.map((p) => p.file.name.split('.')[0]).join(' · '),
      },
      {
        id: '5',
        type: 'card',
        title: 'Greeting Card',
        subtitle: 'With a little something inside',
        badge: 'CARD',
        photoIds: photos.map((p) => p.id),
        madeFrom: photos.map((p) => p.file.name.split('.')[0]).join(' · '),
      },
      {
        id: '6',
        type: 'print',
        title: 'Art Print',
        subtitle: 'Framed and ready to hang',
        badge: 'PRINT',
        photoIds: photos.map((p) => p.id),
        madeFrom: photos.map((p) => p.file.name.split('.')[0]).join(' · '),
      },
    ];

    setProducts(mockProducts);
    setStage('results');
  };

  const getPhotoById = (id: string) => photos.find((p) => p.id === id);

  return (
    <main className="min-h-screen bg-[#090D10] text-[#F5F0E7]">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 p-4 flex items-center gap-2 text-sm tracking-wide">
        <span className="text-[#E3B45D]">✦</span>
        Star at Night
      </header>

      <AnimatePresence mode="wait">
        {stage === 'upload' && (
          <motion.section
            key="upload"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="min-h-screen flex flex-col items-center justify-center px-4 text-center"
          >
            {/* Star */}
            <motion.svg
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="w-24 h-24 mb-8"
              viewBox="0 0 100 100"
              fill="none"
            >
              <circle cx="50" cy="50" r="40" fill="#E3B45D" opacity="0.15" />
              <path
                d="M50 8 L58 38 L88 38 L64 56 L72 86 L50 68 L28 86 L36 56 L12 38 L42 38 Z"
                fill="#E3B45D"
              />
              <circle cx="50" cy="50" r="6" fill="#F2D696" />
            </motion.svg>

            {/* Title */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="font-serif text-5xl md:text-7xl leading-[0.95] tracking-tight mb-4"
            >
              Upload some photos.
              <br />
              We'll make <em className="text-[#F2D696] italic">gifts.</em>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-lg text-[rgba(245,240,231,0.6)] mb-8 max-w-md"
            >
              Drop photos of anyone you love. We'll turn them into newspapers, books, ornaments, and puzzles.
            </motion.p>

            {/* Upload Zone */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              {...getRootProps()}
              className={`w-full max-w-lg border-2 border-dashed rounded-2xl p-12 cursor-pointer transition-all ${
                isDragActive
                  ? 'border-[#E3B45D] bg-[rgba(227,180,93,0.1)]'
                  : 'border-[rgba(245,240,231,0.2)] hover:border-[#E3B45D] hover:bg-[rgba(227,180,93,0.05)]'
              }`}
            >
              <input {...getInputProps()} />
              <div className="text-4xl mb-4 opacity-50">+</div>
              <p className="text-lg mb-2">Drop photos here or tap to browse</p>
              <p className="text-sm text-[rgba(245,240,231,0.4)]">
                JPG, PNG, HEIC — as many as you like
              </p>
            </motion.div>

            {/* Photo Grid */}
            {photos.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-wrap gap-3 justify-center mt-8 max-w-lg"
              >
                {photos.map((photo) => (
                  <motion.img
                    key={photo.id}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    src={photo.preview}
                    alt={photo.file.name}
                    className="w-20 h-20 rounded-xl object-cover shadow-lg"
                  />
                ))}
              </motion.div>
            )}

            {/* Generate Button */}
            {photos.length > 0 && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ y: -2 }}
                onClick={generateProducts}
                className="mt-8 px-8 py-4 bg-[#F5F0E7] text-[#27241F] rounded-full font-medium text-base hover:shadow-lg transition-shadow"
              >
                Make something special →
              </motion.button>
            )}
          </motion.section>
        )}

        {stage === 'generating' && (
          <motion.section
            key="generating"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="min-h-screen flex flex-col items-center justify-center"
          >
            <motion.svg
              animate={{ scale: [1, 1.05, 1], opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-16 h-16 mb-4"
              viewBox="0 0 100 100"
              fill="none"
            >
              <path
                d="M50 8 L58 38 L88 38 L64 56 L72 86 L50 68 L28 86 L36 56 L12 38 L42 38 Z"
                fill="#E3B45D"
              />
              <circle cx="50" cy="50" r="6" fill="#F2D696" />
            </motion.svg>
            <p className="font-serif italic text-lg text-[rgba(245,240,231,0.7)]">
              Creating something special...
            </p>
          </motion.section>
        )}

        {stage === 'results' && (
          <motion.section
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen px-4 py-24 max-w-6xl mx-auto"
          >
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="font-serif text-3xl md:text-4xl text-center mb-12"
            >
              We made {products.length} things from your photos.
            </motion.h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map((product, i) => {
                const photo = getPhotoById(product.photoIds[0]);
                return (
                  <motion.article
                    key={product.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    whileHover={{ y: -4 }}
                    className="bg-[#F5F0E7] rounded-2xl overflow-hidden cursor-pointer"
                  >
                    <div className="aspect-[4/5] bg-[#E9E0D2] flex items-center justify-center p-6 relative">
                      <span className="absolute top-4 left-4 bg-[#27241F] text-[#F5F0E7] text-xs tracking-wider uppercase px-3 py-1.5 rounded-full">
                        {product.badge}
                      </span>
                      {photo && (
                        <img
                          src={photo.preview}
                          alt={product.title}
                          className="max-w-full max-h-full object-contain"
                        />
                      )}
                    </div>
                    <div className="p-5">
                      <h3 className="font-serif text-xl text-[#27241F] mb-1">
                        {product.title}
                      </h3>
                      <p className="text-sm text-[#6F685F] mb-4">{product.subtitle}</p>
                      <p className="text-xs tracking-wider text-[#6F685F] uppercase">
                        Made from {product.madeFrom}
                      </p>
                    </div>
                  </motion.article>
                );
              })}
            </div>

            <div className="text-center mt-12">
              <button
                onClick={() => {
                  useStore.getState().photos = [];
                  useStore.getState().products = [];
                  useStore.getState().stage = 'upload';
                  window.location.reload();
                }}
                className="text-sm text-[rgba(245,240,231,0.5)] hover:text-[#F5F0E7] transition-colors"
              >
                ← Start over with new photos
              </button>
            </div>
          </motion.section>
        )}
      </AnimatePresence>
    </main>
  );
}
