import React from "react";
import imageLoader from "../../utils/imageLoader";

export default function CartItem({
  item,
  increaseQty,
  decreaseQty,
  removeItem
}) {

  return (
    <div className="flex gap-4 border rounded-lg p-4 bg-white">

      <img
        src={item.image || imageLoader.getProductImage(item.name) || imageLoader.FALLBACK_IMAGE}
        alt={item.name}
        className="w-28 h-28 object-cover rounded"
      />

      <div className="flex-1">

        <h3 className="font-semibold text-lg">
          {item.name}
        </h3>

        <p className="text-gray-600">
          ₹{item.price}
        </p>

        <div className="flex items-center gap-3 mt-3">

          <button
            onClick={() => decreaseQty(item.id)}
            className="px-3 py-1 bg-gray-200 rounded"
          >
            -
          </button>

          <span>{item.quantity}</span>

          <button
            onClick={() => increaseQty(item.id)}
            className="px-3 py-1 bg-gray-200 rounded"
          >
            +
          </button>

        </div>

        <button
          onClick={() => removeItem(item.id)}
          className="mt-3 text-red-500"
        >
          Remove
        </button>

      </div>

    </div>
  );
}