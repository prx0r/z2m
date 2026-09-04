import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Star at Night — Upload Photos, We Make Gifts',
  description: 'Drop photos of anyone you love. We'll turn them into newspapers, books, ornaments, and puzzles.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
