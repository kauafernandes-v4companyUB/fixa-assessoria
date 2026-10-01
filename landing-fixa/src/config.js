import content from './content.json'

export const WHATSAPP_NUMBER = (import.meta.env.VITE_WHATSAPP_NUMBER || '').replace(/\D/g, '')
export const WHATSAPP_MESSAGE = content.whatsapp_message

// Sem número configurado, os CTAs levam à seção final em vez de abrir um WhatsApp errado.
export const whatsappHref = WHATSAPP_NUMBER
  ? `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MESSAGE)}`
  : '#contato'

if (!WHATSAPP_NUMBER) {
  console.warn('[landing-fixa] VITE_WHATSAPP_NUMBER não configurado: CTAs apontam para #contato.')
}
