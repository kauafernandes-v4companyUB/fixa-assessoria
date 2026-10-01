import CtaButton from './CtaButton'

export default function Header() {
  return (
    <header className="sticky top-0 z-30 border-b border-linha bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <a href="#topo" className="leading-none" aria-label="Fixa, início da página">
          <span className="block font-display text-2xl font-extrabold tracking-wider text-fixa">FIXA</span>
          <span className="block font-display text-[10px] font-medium tracking-[0.14em] text-grafite">ENGENHARIA &amp; ASSESSORIA</span>
        </a>
        <div className="hidden sm:block">
          <CtaButton location="header" className="px-4 py-2.5 text-base">Fale no WhatsApp</CtaButton>
        </div>
      </div>
    </header>
  )
}
