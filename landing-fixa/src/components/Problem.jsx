import { section } from '../content'
import SectionHead from './SectionHead'

export default function Problem() {
  const s = section('problem')
  return (
    <section className="mx-auto max-w-6xl px-4 py-16 sm:py-20">
      <SectionHead eyebrow={s.eyebrow} headline={s.headline} />
      <div className="grid gap-5 md:grid-cols-3">
        {s.cards?.map((c) => (
          <article key={c.title} className="rounded-xl border border-linha bg-white p-6">
            <h3 className="text-xl font-bold">{c.title}</h3>
            <p className="mt-2 text-tinta/85">{c.body}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
