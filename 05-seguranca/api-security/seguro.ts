import { z } from "zod";

export interface Usuario {
  id: number;
  tenantId: number;
  displayName: string;
  isAdmin: boolean;
}

// .strict() rejeita campos extras (mass assignment) em vez de ignorá-los ou copiá-los.
const AtualizarPerfil = z
  .object({ displayName: z.string().trim().min(1).max(80) })
  .strict();

export function atualizarPerfil(usuario: Usuario, corpo: unknown): Usuario {
  const dados = AtualizarPerfil.parse(corpo);
  usuario.displayName = dados.displayName;
  return usuario;
}
