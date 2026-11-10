/**
 * Cloudflare Worker — receives "Leave a Request" forms from the site
 * and forwards them to a Telegram group (and, optionally, to email via Resend).
 *
 * Secrets / variables to set in Cloudflare (Settings → Variables and Secrets):
 *   TG_TOKEN        — bot token from @BotFather            (type: Secret)
 *   TG_CHAT_ID      — id of the "requests" group, e.g. -1001234567890
 *   ALLOWED_ORIGIN  — the site address, e.g. https://<user>.github.io  (optional; "*" if empty)
 *   RESEND_KEY      — (optional) Resend API key for email   (type: Secret)
 *   MAIL_TO         — (optional) where emails go, e.g. hello@panteleyko.com
 */
export default {
  async fetch(req, env) {
    const origin = env.ALLOWED_ORIGIN || '*';
    const cors = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });

    let d;
    try { d = await req.json(); } catch { return new Response('Bad request', { status: 400, headers: cors }); }

    // honeypot: bots fill the hidden "website" field, people don't
    if (d.website) return new Response('ok', { headers: cors });

    const clean = (v, n = 200) => String(v || '').replace(/[<>]/g, '').trim().slice(0, n);
    const name = clean(d.name), phone = clean(d.phone, 40), email = clean(d.email, 120);
    const service = clean(d.service, 60) || '—', page = clean(d.page, 60);
    if (!name || !email) return new Response('Name and email are required', { status: 422, headers: cors });

    const text =
      `🆕 <b>New request</b>\n\n` +
      `<b>Service:</b> ${service}\n` +
      `<b>Name:</b> ${name}\n` +
      `<b>Email:</b> ${email}\n` +
      (phone ? `<b>Phone:</b> ${phone}\n` : '') +
      (page ? `\n<i>Form: ${page}</i>` : '');

    const jobs = [];
    if (env.TG_TOKEN && env.TG_CHAT_ID) {
      jobs.push(fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: env.TG_CHAT_ID, text, parse_mode: 'HTML' }),
      }));
    }
    if (env.RESEND_KEY && env.MAIL_TO) {
      jobs.push(fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${env.RESEND_KEY}` },
        body: JSON.stringify({
          from: 'Website <onboarding@resend.dev>',
          to: [env.MAIL_TO],
          reply_to: email,
          subject: `New request — ${service} — ${name}`,
          html: text.replace(/\n/g, '<br>'),
        }),
      }));
    }

    const res = await Promise.allSettled(jobs);
    const ok = res.some(r => r.status === 'fulfilled' && r.value.ok);
    return new Response(ok ? 'ok' : 'Delivery failed', { status: ok ? 200 : 502, headers: cors });
  },
};
