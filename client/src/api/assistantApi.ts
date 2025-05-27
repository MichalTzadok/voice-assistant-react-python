export const listenToCommand = async () => {
  const response = await fetch("http://localhost:5000/listen");
  const data = await response.json();
  return data;
};
