const simulatePayment = async ({ method, details, amount }) => {
  await new Promise((resolve) => setTimeout(resolve, 900));

  if (!method) {
    throw new Error("Please select a payment method.");
  }

  if (method === "Credit Card" || method === "Debit Card") {
    if (!details.cardNumber || !details.expiry || !details.cvv) {
      throw new Error("Please enter complete card details.");
    }
  }

  if (method === "UPI" && !details.upiId) {
    throw new Error("Please enter your UPI ID.");
  }

  return {
    status: "success",
    transactionId: `TXN-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    method,
    amount,
    timestamp: new Date().toISOString(),
  };
};

export default { simulatePayment };
