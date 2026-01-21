// pages/api/chat/[userId].js
export default async function handler(req, res) {
  // Get the userId from the query parameters
  const { userId } = req.query;

  // Construct the backend API URL
  const backendUrl = `http://localhost:8000/api/${userId}/chat`;

  if (req.method === 'POST') {
    try {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(req.body),
      });

      const data = await response.json();

      res.status(response.status).json(data);
    } catch (error) {
      res.status(500).json({ error: 'Failed to communicate with backend' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}