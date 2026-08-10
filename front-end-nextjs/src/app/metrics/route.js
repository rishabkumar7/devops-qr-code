import { collectDefaultMetrics, register } from 'prom-client';

export const dynamic = 'force-dynamic';

// Initialize default node/runtime metrics
if (!global._hasInitPrometheus) {
  collectDefaultMetrics();
  global._hasInitPrometheus = true;
}

export async function GET() {
  const metrics = await register.metrics();
  return new Response(metrics, {
    headers: { 'Content-Type': register.contentType },
  });
}
