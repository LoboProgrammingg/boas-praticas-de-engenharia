import { z } from "zod";

export interface Usuario {
  id: number;
  tenantId: number;
  displayName: string;
  isAdmin: boolean;
}

// Objeto "solto": campos desconhecidos passam e o Object.assign copia tudo.
const AtualizarPerfil = z.looseObject({ displayName: z.string().min(1).max(80) });

export function atualizarPerfil(usuario: Usuario, corpo: unknown): Usuario {
  return Object.assign(usuario, AtualizarPerfil.parse(corpo));
}
