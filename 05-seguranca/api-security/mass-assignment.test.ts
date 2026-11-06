import { describe, expect, it } from "vitest";
import { ZodError } from "zod";

import { atualizarPerfil as atualizarSeguro } from "./seguro.js";
import type { Usuario } from "./seguro.js";
import { atualizarPerfil as atualizarVulneravel } from "./vulneravel.js";

function novoUsuario(): Usuario {
  return { id: 1, tenantId: 10, displayName: "Ana", isAdmin: false };
}

describe("mass assignment", () => {
  it("vulneravel: o cliente vira admin e troca de tenant", () => {
    const usuario = atualizarVulneravel(novoUsuario(), {
      displayName: "Ana",
      isAdmin: true,
      tenantId: 99,
    });

    expect(usuario.isAdmin).toBe(true);
    expect(usuario.tenantId).toBe(99);
  });

  it("seguro: rejeita campos extras e não altera o usuário", () => {
    const usuario = novoUsuario();

    expect(() => atualizarSeguro(usuario, { displayName: "Ana", isAdmin: true })).toThrow(ZodError);
    expect(usuario.isAdmin).toBe(false);
  });

  it("seguro: atualiza só o campo permitido, já sem espaços nas pontas", () => {
    const usuario = atualizarSeguro(novoUsuario(), { displayName: "  Ana Souza  " });

    expect(usuario.displayName).toBe("Ana Souza");
    expect(usuario.tenantId).toBe(10);
  });

  it("seguro: valida o tamanho do campo", () => {
    expect(() => atualizarSeguro(novoUsuario(), { displayName: "" })).toThrow(ZodError);
    expect(() => atualizarSeguro(novoUsuario(), { displayName: "x".repeat(81) })).toThrow(ZodError);
  });
});
