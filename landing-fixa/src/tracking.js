// Carrega GA4 e pixel da Meta só quando os IDs estiverem configurados.
export function initTracking() {
  const ga4 = import.meta.env.VITE_GA4_ID
  const pixel = import.meta.env.VITE_META_PIXEL_ID

  if (ga4) {
    const s = document.createElement('script')
    s.async = true
    s.src = `https://www.googletagmanager.com/gtag/js?id=${ga4}`
    document.head.appendChild(s)
    window.dataLayer = window.dataLayer || []
    window.gtag = function () { window.dataLayer.push(arguments) }
    window.gtag('js', new Date())
    window.gtag('config', ga4)
  }

  if (pixel) {
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq('init', pixel)
    window.fbq('track', 'PageView')
  }
}

// Clique em qualquer CTA de WhatsApp vira conversão (GA4: generate_lead, Meta: Contact).
export function trackWhatsappClick(location) {
  if (window.gtag) window.gtag('event', 'generate_lead', { method: 'whatsapp', location })
  if (window.fbq) window.fbq('track', 'Contact', { location })
}
