import type { VercelRequest, VercelResponse } from '@vercel/node';

const API_KEY = process.env.ECHO_API_KEY;

function generateId(): string {
  return `echo-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: { message: 'Method not allowed', type: 'invalid_request_error' } });
  }

  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: { message: 'Missing Authorization header', type: 'authentication_error' } });
  }

  const token = authHeader.substring(7);
  if (API_KEY && token !== API_KEY) {
    return res.status(401).json({ error: { message: 'Invalid API key', type: 'authentication_error' } });
  }

  let body: unknown;
  try {
    body = req.body;
  } catch {
    return res.status(400).json({ error: { message: 'Invalid JSON body', type: 'invalid_request_error' } });
  }

  const response = {
    id: generateId(),
    object: 'chat.completion',
    created: Math.floor(Date.now() / 1000),
    model: 'echo',
    choices: [
      {
        index: 0,
        message: {
          role: 'assistant',
          content: JSON.stringify(body, null, 2),
        },
        finish_reason: 'stop',
      },
    ],
    usage: {
      prompt_tokens: 0,
      completion_tokens: 0,
      total_tokens: 0,
    },
  };

  return res.status(200).json(response);
}
