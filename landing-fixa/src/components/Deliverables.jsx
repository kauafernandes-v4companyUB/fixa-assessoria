import { Check } from 'lucide-react'
import { section } from '../content'
import SectionHead from './SectionHead'

export default function Deliverables() {
  const s = section('deliverables')
  return (
    <section className="mx-auto max-w-6xl px-4 py-16 sm:py-20">
      <SectionHead eyebrow={s.eyebrow} headline={s.headline} />
      <ul className="grid gap-4 md:grid-cols-2">
        {s.items?.map((it) => (
          <li key={it.title} className="flex gap-3 rounded-xl border border-linha p-5">
            <Check aria-hidden="true" className="mt-1 h-5 w-5 shrink-0 text-serra" strokeWidth={2.5} />
            <div>
              <p className="font-display font-bold text-fixa">{it.title}</p>
              <p className="text-base text-grafite">{it.benefit}</p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}
