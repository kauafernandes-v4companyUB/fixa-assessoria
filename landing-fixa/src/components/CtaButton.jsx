import { MessageCircle } from 'lucide-react'
import { whatsappHref, WHATSAPP_NUMBER } from '../config'
import { trackWhatsappClick } from '../tracking'

export default function CtaButton({ children, location, variant = 'primary', className = '' }) {
  const styles = {
    primary: 'bg-serra text-white hover:bg-fixa',
    light: 'bg-white text-fixa hover:bg-nevoa',
  }
  const external = Boolean(WHATSAPP_NUMBER)
  return (
    <a
      href={whatsappHref}
      target={external ? '_blank' : undefined}
      rel={external ? 'noopener noreferrer' : undefined}
      onClick={() => trackWhatsappClick(location)}
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-6 py-4 font-display text-lg font-bold transition-colors focus:outline-none focus-visible:ring-4 focus-visible:ring-serra/40 ${styles[variant]} ${className}`}
    >
      <MessageCircle aria-hidden="true" className="h-5 w-5" />
      {children}
    </a>
  )
}
