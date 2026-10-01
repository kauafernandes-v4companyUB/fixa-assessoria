import { section } from '../content'
import SectionHead from './SectionHead'
import CtaButton from './CtaButton'

export default function HowItWorks() {
  const s = section('how_it_works')
  return (
    <section id="como-funciona" className="mx-auto max-w-6xl scroll-mt-20 px-4 py-16 sm:py-20">
      <SectionHead eyebrow={s.eyebrow} headline={s.headline} />
      <ol className="grid gap-6 md:grid-cols-3">
        {s.steps?.map((st) => (
          <li key={st.number} className="rounded-xl bg-nevoa p-6">
            <span className="font-display text-5xl font-extrabold text-serra">{st.number}</span>
            <h3 className="mt-3 text-xl font-bold">{st.title}</h3>
            <p className="mt-2 text-tinta/85">{st.body}</p>
          </li>
        ))}
      </ol>
      <div className="mt-10">
        <CtaButton location="como_funciona">Contar meu caso no WhatsApp</CtaButton>
      </div>
    </section>
  )
}
