import { MessageCircle } from 'lucide-react'
import { whatsappHref, WHATSAPP_NUMBER } from '../config'
import { trackWhatsappClick } from '../tracking'

// Botão fixo só no celular, onde o CTA do header fica escondido.
export default function WhatsappFloat() {
  const external = Boolean(WHATSAPP_NUMBER)
  return (
    <a
      href={whatsappHref}
      target={external ? '_blank' : undefined}
      rel={external ? 'noopener noreferrer' : undefined}
      onClick={() => trackWhatsappClick('flutuante')}
      aria-label="Falar com a Fixa no WhatsApp"
      className="fixed bottom-4 right-4 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-serra text-white shadow-lg sm:hidden"
    >
      <MessageCircle aria-hidden="true" className="h-7 w-7" />
    </a>
  )
}
