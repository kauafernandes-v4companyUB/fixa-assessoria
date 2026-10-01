import { ChevronDown } from 'lucide-react'
import { section, faq } from '../content'
import SectionHead from './SectionHead'

export default function Faq() {
  const s = section('faq')
  return (
    <section className="mx-auto max-w-3xl px-4 py-16 sm:py-20">
      <SectionHead eyebrow={s.eyebrow} headline={s.headline} />
      <div className="divide-y divide-linha border-y border-linha">
        {faq.map((q) => (
          <details key={q.question} className="group py-5">
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4 font-display text-lg font-bold text-fixa [&::-webkit-details-marker]:hidden">
              {q.question}
              <ChevronDown aria-hidden="true" className="h-5 w-5 shrink-0 text-serra transition-transform group-open:rotate-180" />
            </summary>
            <p className="mt-3 text-tinta/85">{q.answer}</p>
          </details>
        ))}
      </div>
    </section>
  )
}
