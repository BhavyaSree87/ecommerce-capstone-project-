import placeholderImage from '../assets/images/product-placeholder.svg';

const imageModules = import.meta.glob('../assets/images/*.{jpg,jpeg,png,webp}', {
  eager: true,
  import: 'default',
});

const FALLBACK_IMAGE = placeholderImage;

const normalizeFileName = (name) => {
  if (!name) return '';
  return name
    .toString()
    .toLowerCase()
    .replace(/['’‘]/g, '')
    .replace(/[()\[\]{}]/g, '')
    .replace(/[-_]/g, ' ')
    .replace(/[.,/\\]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
};

const buildImageMap = () => {
  const map = {};

  Object.entries(imageModules).forEach(([filePath, fileUrl]) => {
    const fileName = filePath.split('/').pop();
    const normalized = normalizeFileName(fileName.replace(/\.[^.]+$/, ''));
    if (normalized) {
      map[normalized] = fileUrl;
    }
  });

  return map;
};

const imageMap = buildImageMap();

const getProductImage = (productName) => {
  return imageMap[normalizeFileName(productName)] || FALLBACK_IMAGE;
};

const getProductImages = (productName) => {
  return [getProductImage(productName)];
};

export default {
  getProductImage,
  getProductImages,
  FALLBACK_IMAGE,
  normalizeFileName,
};
