export const categories = [
  {
    title: "Men",
    image:
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f",
    count: 120,
  },
  {
    title: "Women",
    image:
      "https://images.unsplash.com/photo-1496747611176-843222e1e57c",
    count: 210,
  },
  {
    title: "Kids",
    image:
      "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea",
    count: 80,
  },
  {
    title: "Footwear",
    image:
      "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
    count: 95,
  },
  {
    title: "Accessories",
    image:
      "https://images.unsplash.com/photo-1523170335258-f5ed11844a49",
    count: 60,
  },
  {
    title: "Beauty",
    image:
      "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9",
    count: 40,
  },
];

const products = [
  {
    id: "p1",
    brand: "Urban Threads",
    name: "Slim Fit Casual Shirt",
    price: 1499,
    discount: 20,
    rating: 4.3,
    images: [
      "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1521334884684-d80222895322?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["S", "M", "L", "XL"],
    colors: ["#111827", "#F97316", "#9333EA"],
    category: "Men",
    zone: "Casual Wear",
    description:
      "Classic slim fit shirt in breathable cotton blend, perfect for everyday styling and office-casual looks.",
  },
  {
    id: "p2",
    brand: "Elle & Co",
    name: "Floral Summer Dress",
    price: 2499,
    discount: 15,
    rating: 4.6,
    images: [
      "https://th.bing.com/th/id/OIP.mLDJQpKT9krVE0qL1F44BgHaKh?w=202&h=287&c=7&r=0&o=7&pid=1.7&rm=3",
    ],
    sizes: ["XS", "S", "M", "L"],
    colors: ["#F43F5E", "#06B6D4"],
    category: "Women",
    zone: "Party Wear",
    description:
      "Lightweight floral dress with a feminine silhouette, ideal for day parties and weekend brunches.",
  },
  {
    id: "p3",
    brand: "Stride",
    name: "Running Shoes X1",
    price: 3999,
    discount: 25,
    rating: 4.5,
    images: [
      "data:image/webp;base64,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",
    ],
    sizes: ["7", "8", "9", "10"],
    colors: ["#000000", "#10B981"],
    category: "Footwear",
    zone: "Sportswear",
    description:
      "Lightweight running trainers with responsive cushioning and breathable mesh for daily runs.",
  },
  {
    id: "p4",
    brand: "Luxe Bags",
    name: "City Leather Handbag",
    price: 5299,
    discount: 18,
    rating: 4.7,
    images: [
      "https://th.bing.com/th/id/OIP.8LyHnrSNtGmdkbpEbE2K4QHaHa?w=202&h=202&c=7&r=0&o=7&pid=1.7&rm=3",
    ],
    sizes: ["One Size"],
    colors: ["#A855F7", "#F97316"],
    category: "Accessories",
    zone: "Everyday Lux",
    description:
      "Structured leather handbag with polished hardware and a roomy interior for everyday essentials.",
  },
  {
    id: "p5",
    brand: "Timepiece",
    name: "Classic Chronograph Watch",
    price: 7999,
    discount: 10,
    rating: 4.8,
    images: [
      "https://images.unsplash.com/photo-1516728778615-2d590ea1856f?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1543163521-1bf5396c4e58?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["One Size"],
    colors: ["#111827", "#F59E0B"],
    category: "Accessories",
    zone: "Formal Wear",
    description:
      "Elegant chronograph watch with premium finish and versatile styling for office and evening wear.",
  },
  {
    id: "p6",
    brand: "Glow Beauty",
    name: "Nourishing Skin Serum",
    price: 1299,
    discount: 12,
    rating: 4.4,
    images: [
      "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["30ml", "50ml"],
    colors: ["#FBCFE8", "#BFDBFE"],
    category: "Beauty",
    zone: "Skincare",
    description:
      "Hydrating serum enriched with botanical extracts to brighten and restore skin radiance.",
  },
  {
    id: "p7",
    brand: "Denim Lab",
    name: "Retro Denim Jacket",
    price: 3599,
    discount: 22,
    rating: 4.5,
    images: [
      "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["S", "M", "L", "XL"],
    colors: ["#1F2937", "#6B7280"],
    category: "Men",
    zone: "Layering",
    description:
      "Classic denim jacket with a relaxed fit and durable wash, perfect for layering through the seasons.",
  },
  {
    id: "p8",
    brand: "Peak Active",
    name: "Core Performance Hoodie",
    price: 2799,
    discount: 18,
    rating: 4.4,
    images: [
      "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1490727561557-8feec2d04806?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["S", "M", "L", "XL"],
    colors: ["#0F172A", "#10B981"],
    category: "Men",
    zone: "Athleisure",
    description:
      "Comfortable hoodie engineered for movement and everyday street-style appeal.",
  },
  {
    id: "p9",
    brand: "Nova Steps",
    name: "Everyday Sneakers",
    price: 4399,
    discount: 20,
    rating: 4.6,
    images: [
      "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["7", "8", "9", "10"],
    colors: ["#111827", "#F97316"],
    category: "Footwear",
    zone: "Streetwear",
    description:
      "Versatile sneakers with cushioned support and a bold profile for daily city wear.",
  },
  {
    id: "p10",
    brand: "Bloom Box",
    name: "Beauty Essentials Kit",
    price: 2399,
    discount: 14,
    rating: 4.5,
    images: [
      "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=900&q=80",
    ],
    sizes: ["Standard"],
    colors: ["#F9A8D4", "#C084FC"],
    category: "Beauty",
    zone: "Beauty",
    description:
      "Curated kit with essential skincare and makeup favorites for effortless glam routines.",
  },
];

export default products;

