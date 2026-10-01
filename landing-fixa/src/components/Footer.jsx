export default function Footer() {
  return (
    <footer className="bg-tinta text-white/70">
      <div className="mx-auto max-w-6xl px-4 py-10 text-sm">
        <p className="font-display text-lg font-extrabold tracking-wider text-white">FIXA</p>
        <p className="mt-1">Engenharia e direito, num processo só. Caxias do Sul e Serra Gaúcha.</p>
        {/* Rodapé legal: completar com os CNPJs das duas razões sociais antes do deploy. */}
        <p className="mt-6 text-[13px] font-semibold">Fixa Engenharia Ltda · Fixa Assessoria Ltda</p>
      </div>
    </footer>
  )
}
