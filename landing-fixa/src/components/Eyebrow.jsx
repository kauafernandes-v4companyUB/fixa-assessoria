export default function Eyebrow({ children, light = false }) {
  if (!children) return null
  return (
    <p className={`mb-3 font-display text-[13px] font-semibold uppercase tracking-[0.08em] ${light ? 'text-white/80' : 'text-serra'}`}>
      {children}
    </p>
  )
}
