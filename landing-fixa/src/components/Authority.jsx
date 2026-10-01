import { section } from '../content'
import SectionHead from './SectionHead'

export default function Authority() {
  const s = section('authority')
  return (
    <section className="border-y border-linha bg-nevoa">
      <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:py-20 lg:grid-cols-2">
        <div>
          <SectionHead eyebrow={s.eyebrow} headline={s.headline} />
          <p className="text-tinta/90">{s.body}</p>
          {s.credential_card && (
            <div className="mt-6 inline-block rounded-lg border-l-4 border-serra bg-white px-5 py-3">
              <p className="font-display font-bold text-fixa">{s.credential_card.name}</p>
              <p className="text-base text-grafite">{s.credential_card.role}</p>
            </div>
          )}
        </div>
        <ol className="relative space-y-6 border-l-2 border-linha pl-6 lg:mt-14">
          {s.credentials?.map((c) => (
            <li key={c.year} className="relative">
              <span className="absolute -left-[33px] top-1.5 h-4 w-4 rounded-full border-4 border-nevoa bg-serra" aria-hidden="true" />
              <p className="font-display text-sm font-bold text-serra">{c.year}</p>
              <p className="text-tinta">{c.title}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
