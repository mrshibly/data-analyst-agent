import type { ChatMessage } from '../types';

// detect if we are in development or production
const isDev = import.meta.env.DEV;
const API_BASE = isDev ? 'http://127.0.0.1:8000/api/v1' : '/api/v1';

export function getChartUrl(path: string) {
  if (path.startsWith('http')) return path;
  if (isDev) return `http://127.0.0.1:8000${path}`;
  return path;
}

export async function uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }

  return response.json();
}

export async function analyzeQueryStream(
  fileId: string,
  query: string,
  onEvent: (event: string, data: any) => void,
  chatHistory: ChatMessage[] = []
) {
  // Use EventSource (GET) for maximum reliability with SSE
  const historyParam = chatHistory.length > 0 ? `&history=${encodeURIComponent(JSON.stringify(chatHistory))}` : '';
  const url = `${API_BASE}/analyze/stream?file_id=${fileId}&query=${encodeURIComponent(query)}${historyParam}`;
  
  return new Promise<void>((resolve, reject) => {
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onEvent('message', data);
      } catch (e) {
        onEvent('message', event.data);
      }
    };

    // Handle our named events
    const eventTypes = ['status', 'thought', 'chart', 'statistics', 'final_result', 'error'];
    eventTypes.forEach(type => {
      eventSource.addEventListener(type, (event: any) => {
        if (type === 'final_result') {
          try {
            const data = JSON.parse(event.data);
            onEvent(type, data);
            eventSource.close();
            resolve();
          } catch (e) {
            console.error('Final result parse error:', e);
            eventSource.close();
            resolve();
          }
        } else if (type === 'error') {
          try {
            const data = JSON.parse(event.data);
            onEvent(type, data);
            eventSource.close();
            reject(new Error(data.detail || 'Analysis stream failed'));
          } catch (e) {
            eventSource.close();
            reject(new Error('Analysis stream failed'));
          }
        } else {
          try {
            const data = JSON.parse(event.data);
            onEvent(type, data);
          } catch (e) {
            onEvent(type, event.data);
          }
        }
      });
    });

    eventSource.onerror = (err) => {
      console.error('EventSource failed:', err);
      eventSource.close();
      // If we haven't resolved yet, this is a fatal connection error
      reject(new Error('Network disruption: Connection to analytical engine reset.'));
    };
  });
}

