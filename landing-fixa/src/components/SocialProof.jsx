import { PlayCircle } from 'lucide-react'
import { section, socialProof } from '../content'
import SectionHead from './SectionHead'

// Os números ficam no hero; aqui entram só os casos com nome (sem citação inventada).
export default function SocialProof() {
  const s = section('social_proof')
  const cases = socialProof.cases || []
  return (
    <section className="bg-nevoa">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:py-20">
        <SectionHead eyebrow={s.eyebrow} headline={s.headline} />
        <div className="grid gap-5 md:grid-cols-2">
          {cases.map((c) => (
            <article key={c.name} className="flex flex-col rounded-xl border-t-4 border-serra bg-white p-6">
              <h3 className="text-xl font-bold">{c.name}</h3>
              <p className="mt-2 flex-1 text-tinta/85">{c.what}</p>
              <a
                href={c.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-5 inline-flex items-center gap-2 font-display font-bold text-serra hover:text-fixa"
              >
                <PlayCircle aria-hidden="true" className="h-5 w-5" />
                Ver o depoimento de {c.person}
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
