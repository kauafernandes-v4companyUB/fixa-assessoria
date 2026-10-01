import { Layers, Landmark, ListChecks, KeyRound } from 'lucide-react'
import { section } from '../content'
import SectionHead from './SectionHead'

const ICONS = { Layers, Landmark, ListChecks, KeyRound }

export default function Solution() {
  const s = section('solution')
  return (
    <section className="bg-fixa text-white">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:py-20">
        <SectionHead eyebrow={s.eyebrow} headline={s.headline} light />
        <div className="grid gap-8 sm:grid-cols-2">
          {s.benefits?.map((b) => {
            const Icon = ICONS[b.icon] || Layers
            return (
              <div key={b.title} className="flex gap-4">
                <Icon aria-hidden="true" strokeWidth={2} className="mt-1 h-7 w-7 shrink-0 text-white/90" />
                <div>
                  <h3 className="text-xl font-bold text-white">{b.title}</h3>
                  <p className="mt-1 text-white/85">{b.body}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
