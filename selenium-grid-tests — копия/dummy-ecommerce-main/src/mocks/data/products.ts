import { Product } from "@/types";

export const products: Product[] = [
  {
    id: "prod-001",
    name: "Wireless Headphones",
    description:
      "Premium over-ear wireless headphones with active noise cancellation and 30-hour battery life.",
    price: 7999,
    category: "electronics",
    image: "https://placehold.co/300x300/1a1a2e/e0e0e0?text=Headphones",
    inStock: true,
  },
  {
    id: "prod-002",
    name: "Bluetooth Speaker",
    description:
      "Portable waterproof Bluetooth speaker with 360-degree sound and 12-hour playtime.",
    price: 4999,
    category: "electronics",
    image: "https://placehold.co/300x300/1a1a2e/e0e0e0?text=Speaker",
    inStock: true,
  },
  {
    id: "prod-003",
    name: "USB-C Hub",
    description:
      "7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and 100W power delivery.",
    price: 3499,
    category: "electronics",
    image: "https://placehold.co/300x300/1a1a2e/e0e0e0?text=USB-C+Hub",
    inStock: true,
  },
  {
    id: "prod-004",
    name: "Mechanical Keyboard",
    description:
      "Full-size mechanical keyboard with Cherry MX Blue switches and RGB backlighting.",
    price: 12999,
    category: "electronics",
    image: "https://placehold.co/300x300/1a1a2e/e0e0e0?text=Keyboard",
    inStock: true,
  },
  {
    id: "prod-005",
    name: "Cotton T-Shirt",
    description:
      "Classic fit 100% organic cotton t-shirt. Soft, breathable, and available in multiple colors.",
    price: 1999,
    category: "clothing",
    image: "https://placehold.co/300x300/2d4a22/e0e0e0?text=T-Shirt",
    inStock: true,
  },
  {
    id: "prod-006",
    name: "Denim Jacket",
    description:
      "Vintage-style denim jacket with a modern slim fit. Features button closure and chest pockets.",
    price: 8999,
    category: "clothing",
    image: "https://placehold.co/300x300/2d4a22/e0e0e0?text=Denim+Jacket",
    inStock: true,
  },
  {
    id: "prod-007",
    name: "Running Shoes",
    description:
      "Lightweight running shoes with responsive cushioning and breathable mesh upper.",
    price: 6499,
    category: "clothing",
    image: "https://placehold.co/300x300/2d4a22/e0e0e0?text=Shoes",
    inStock: true,
  },
  {
    id: "prod-008",
    name: "Wool Beanie",
    description:
      "Warm merino wool beanie hat. Double-layered for extra warmth during cold weather.",
    price: 1499,
    category: "clothing",
    image: "https://placehold.co/300x300/2d4a22/e0e0e0?text=Beanie",
    inStock: false,
  },
  {
    id: "prod-009",
    name: "Ceramic Mug",
    description:
      "Handcrafted ceramic mug with a 12oz capacity. Microwave and dishwasher safe.",
    price: 1299,
    category: "home",
    image: "https://placehold.co/300x300/4a2222/e0e0e0?text=Mug",
    inStock: true,
  },
  {
    id: "prod-010",
    name: "Scented Candle",
    description:
      "Soy wax scented candle with lavender and vanilla fragrance. Burns for up to 50 hours.",
    price: 2499,
    category: "home",
    image: "https://placehold.co/300x300/4a2222/e0e0e0?text=Candle",
    inStock: true,
  },
  {
    id: "prod-011",
    name: "Throw Pillow",
    description:
      "Decorative throw pillow with removable cotton cover. 18x18 inches.",
    price: 2999,
    category: "home",
    image: "https://placehold.co/300x300/4a2222/e0e0e0?text=Pillow",
    inStock: true,
  },
  {
    id: "prod-012",
    name: "JavaScript Guide",
    description:
      "Comprehensive guide to modern JavaScript. Covers ES6+, async patterns, and best practices.",
    price: 3999,
    category: "books",
    image: "https://placehold.co/300x300/22224a/e0e0e0?text=JS+Guide",
    inStock: true,
  },
  {
    id: "prod-013",
    name: "Cooking Basics",
    description:
      "Essential cookbook for beginners with 200+ easy-to-follow recipes and cooking techniques.",
    price: 2499,
    category: "books",
    image: "https://placehold.co/300x300/22224a/e0e0e0?text=Cookbook",
    inStock: true,
  },
  {
    id: "prod-014",
    name: "Sci-Fi Novel",
    description:
      "Award-winning science fiction novel set in a distant future. A gripping tale of exploration.",
    price: 1499,
    category: "books",
    image: "https://placehold.co/300x300/22224a/e0e0e0?text=Sci-Fi",
    inStock: true,
  },
];

export const categories = ["electronics", "clothing", "home", "books"];
