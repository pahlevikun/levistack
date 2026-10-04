#!/usr/bin/env python3
"""Add register examples and natural grammar to wave-2 language packs."""

from __future__ import annotations

from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
LANG = SKILL_ROOT / "references" / "languages"

PACKS = {
    "mandarin": {
        "pronouns": "我 / 我们；你 (peer) vs 您 (respect/work). Overlay picks 简体/繁體.",
        "baku_good": "谨通知：服务将于周二维护期间暂停。",
        "baku_bad": "The service will be down Tuesday — English SVO pasted.",
        "prof_good": "原因是 `.env` 里没有 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。",
        "prof_bad": "Kindly revert regarding the token.",
        "santai_good": "`.env` 里没配 `API_TOKEN`，跑一下 `npm test -- config`。",
        "santai_bad": "网络用语堆砌或 fake 梗.",
        "natural": (
            "1. **Topic-comment** — 先说主题再展开.\n"
            "2. **了/过/着** aspect — 完成用「了」，不要英语过去式直译.\n"
            "3. **在/于 location** — `在 .env 里`.\n"
            "4. **把 construction** — `把 token 配好`.\n"
            "5. **请 vs 麻烦** — 工作里一次就够.\n"
            "6. **简体/繁体** — overlay 决定，不混写.\n"
            "7. **技术词** — 保留 repo 字面量."
        ),
    },
    "hindi": {
        "pronouns": "मैं / हम; तुम (close) vs आप (work).",
        "baku_good": "सूचित किया जाता है कि मंगलवार को रखरखाव के लिए सेवा बंद रहेगी।",
        "baku_bad": "Service will be down — English order.",
        "prof_good": "`API_TOKEN` `.env` में नहीं है, इसलिए `loadConfig` `undefined` लौटाता है।",
        "prof_bad": "Kindly revert.",
        "santai_good": "`API_TOKEN` `.env` में नहीं — `npm test -- config` चला लो।",
        "santai_bad": "Hinglish every word without ask.",
        "natural": (
            "1. **SOV** — क्रिया अंत में.\n"
            "2. **में/पर postpositions**.\n"
            "3. **नहीं negation**.\n"
            "4. **आप honorific verbs**.\n"
            "5. **कर दो causative**.\n"
            "6. **Hinglish mix** — overlay only.\n"
            "7. **Code literals** exact."
        ),
    },
    "spanish": {
        "pronouns": "yo / nosotros; tú (peer) vs usted (work external).",
        "baku_good": "Se informa que el servicio estará indisponible el martes por mantenimiento.",
        "baku_bad": "The service will be down Tuesday — English calque.",
        "prof_good": "Falta `API_TOKEN` en `.env`, así que `loadConfig` devuelve `undefined`.",
        "prof_bad": "Kindly revert the configuration.",
        "santai_good": "No está el `API_TOKEN` en `.env` — corre `npm test -- config`.",
        "santai_bad": "Random regional slang mix (es-ar + es-mx).",
        "natural": (
            "1. **Flexible SVO** — keep natural clitics.\n"
            "2. **Por/para** — reason vs purpose.\n"
            "3. **Subjunctive** for soft asks — one per message max.\n"
            "4. **tú/usted** — lock per message.\n"
            "5. **Overlay vocabulary** — Spain vs Mexico.\n"
            "6. **No English -ing calques**.\n"
            "7. **Technical literals** unchanged."
        ),
    },
    "french": {
        "pronouns": "je / nous; tu (peer) vs vous (work).",
        "baku_good": "Nous vous informons que le service sera indisponible mardi pour maintenance.",
        "baku_bad": "Service will be down Tuesday — English pasted.",
        "prof_good": "`API_TOKEN` manque dans `.env`, donc `loadConfig` renvoie `undefined`.",
        "prof_bad": "Kindly revert.",
        "santai_good": "Il n'y a pas de `API_TOKEN` dans `.env` — lance `npm test -- config`.",
        "santai_bad": "Franglais every noun.",
        "natural": (
            "1. **Negation ne…pas** — both parts.\n"
            "2. **Articles** — le/la/les with natural gender.\n"
            "3. **Vous verbs** in work external.\n"
            "4. **On for we** in casual internal OK.\n"
            "5. **Subjunctive** after il faut que — sparingly.\n"
            "6. **fr-fr overlay** for lexicon.\n"
            "7. **Code literals** Latin."
        ),
    },
    "portuguese": {
        "pronouns": "eu / nós; tu/você (BR) vs você (formal).",
        "baku_good": "Informamos que o serviço ficará indisponível na terça-feira para manutenção.",
        "baku_bad": "Service will be down — English order.",
        "prof_good": "`API_TOKEN` não está no `.env`, então `loadConfig` retorna `undefined`.",
        "prof_bad": "Kindly revert.",
        "santai_good": "Não tem `API_TOKEN` no `.env` — roda `npm test -- config`.",
        "santai_bad": "pt-pt and pt-br mixed without overlay.",
        "natural": (
            "1. **Proclitic pronouns** in BR — natural placement.\n"
            "2. **estar vs ser** — state vs identity.\n"
            "3. **pt-br overlay** for informal.\n"
            "4. **não negation** before verb.\n"
            "5. **Por/para** distinction.\n"
            "6. **No tu in BR work** unless user asks.\n"
            "7. **Technical literals** exact."
        ),
    },
    "japanese": {
        "pronouns": "私/僕 (context); あなた sparingly — name + さん in work.",
        "baku_good": "火曜日のメンテナンスのため、サービスを停止します。",
        "baku_bad": "Service will be down Tuesday — English SVO.",
        "prof_good": "`.env` に `API_TOKEN` がないため、`loadConfig` は `undefined` を返します。",
        "prof_bad": "Kindly revert.",
        "santai_good": "`.env` に `API_TOKEN` ないから、`npm test -- config` 走らせて。",
        "santai_bad": "Invented keigo chain without examples.",
        "natural": (
            "1. **です/ます default** in work — ため口 only when asked.\n"
            "2. **は topic particle** — don't drop blindly.\n"
            "3. **ので/から reason** — natural cause.\n"
            "4. **Keigo** — thin without user examples.\n"
            "5. **Soft CTA** — ご確認ください vs hard sell.\n"
            "6. **No subject if clear** from context.\n"
            "7. **Code literals** unchanged."
        ),
    },
    "korean": {
        "pronouns": "저/제가 (humble); 너/당신 avoid in work — name + title.",
        "baku_good": "화요일 점검으로 서비스가 중단됩니다.",
        "baku_bad": "Service will be down — English calque.",
        "prof_good": "`.env`에 `API_TOKEN`이 없어서 `loadConfig`가 `undefined`를 반환합니다.",
        "prof_bad": "Kindly revert.",
        "santai_good": "`.env`에 `API_TOKEN` 없어 — `npm test -- config` 돌려.",
        "santai_bad": "반말 to executives without signal.",
        "natural": (
            "1. **SOV** — verb final.\n"
            "2. **-요 polite default** in work.\n"
            "3. **-아/어서 cause** — natural reason.\n"
            "4. **존댓말/반말** — lock per message.\n"
            "5. **Topic marker 는/은**.\n"
            "6. **No English -ing** calque.\n"
            "7. **Technical literals** exact."
        ),
    },
    "vietnamese": {
        "pronouns": "tôi / chúng tôi; bạn (peer) vs anh/chị + name (respect).",
        "baku_good": "Thông báo: dịch vụ sẽ ngừng vào thứ Ba để bảo trì.",
        "baku_bad": "Service will be down — English order.",
        "prof_good": "`API_TOKEN` không có trong `.env`, nên `loadConfig` trả về `undefined`.",
        "prof_bad": "Kindly revert.",
        "santai_good": "`.env` chưa có `API_TOKEN` — chạy `npm test -- config`.",
        "santai_bad": "Random kinship pronouns without relationship.",
        "natural": (
            "1. **Kinship pronouns** — only when relationship clear.\n"
            "2. **không negation** before verb.\n"
            "3. **trong/ở location** — `trong .env`.\n"
            "4. **SVO default**.\n"
            "5. **anh/chị** respect in work external.\n"
            "6. **Classifiers** for objects when natural.\n"
            "7. **Technical literals** exact."
        ),
    },
    "tagalog": {
        "pronouns": "ako / kami; ikaw (close) vs po/ho respect particles in work.",
        "baku_good": "Ipinapaalam na ang serbisyo ay hindi magagamit sa Martes para sa maintenance.",
        "baku_bad": "Service will be down — English pasted.",
        "prof_good": "Wala ang `API_TOKEN` sa `.env`, kaya `undefined` ang ibinabalik ng `loadConfig`.",
        "prof_bad": "Kindly revert.",
        "santai_good": "Walang `API_TOKEN` sa `.env` — patakbuhin ang `npm test -- config`.",
        "santai_bad": "Taglish every word without overlay.",
        "natural": (
            "1. **Ang topic focus** — natural word order.\n"
            "2. **walang/wala** for absence.\n"
            "3. **po/ho** — respect, not every word.\n"
            "4. **Taglish overlay** only on ask.\n"
            "5. **ng/na ligatures** — natural.\n"
            "6. **Soft asks** — puwede po ba.\n"
            "7. **Technical literals** exact."
        ),
    },
}


def write_registers(lang_id: str, data: dict) -> None:
    text = f"""# {lang_id} registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

{data["pronouns"]}

## Examples

### `baku` (formal)

- **Good:** {data["baku_good"]}
- **Bad:** {data["baku_bad"]}

### `profesional` (work)

- **Good:** {data["prof_good"]}
- **Bad:** {data["prof_bad"]}

### `santai` (casual)

- **Good:** {data["santai_good"]}
- **Bad:** {data["santai_bad"]}

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
"""
    (LANG / lang_id / "registers.md").write_text(text, encoding="utf-8")


def patch_culture(lang_id: str, natural: str) -> None:
    path = LANG / lang_id / "culture.md"
    text = path.read_text(encoding="utf-8")
    if "## Natural grammar" in text:
        return
    if "## Do not copy from English corporate" in text:
        text = text.replace(
            "## Do not copy from English corporate",
            f"## Natural grammar\n\n{natural}\n\n## Do not copy from English corporate",
        )
    else:
        text += f"\n\n## Natural grammar\n\n{natural}\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for lang_id, data in PACKS.items():
        write_registers(lang_id, data)
        patch_culture(lang_id, data["natural"])
    print(f"Improved {len(PACKS)} wave-2 language packs.")


if __name__ == "__main__":
    main()
