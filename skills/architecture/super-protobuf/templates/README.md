# Templates

Copy and adapt. Language options stay in `buf.gen.yaml` (managed mode), not in these files.

| File | What it is |
|------|------------|
| `resource.proto` | AIP-style resource + enum + Ref oneof + protovalidate |
| `service.proto` | One service per file: Get/List/Create/Update/Delete |
| `buf.yaml` | Module, STANDARD lint, FILE breaking, protovalidate dep |

Worked book example (CRUD + batch): `assets/proto/example/v1/book.proto`, `book_service.proto`.

Buf gen starters in `assets/`: `buf.yaml`, `buf.lock`, `buf.gen.yaml`, `buf.gen.go.yaml`, `buf.gen.go-connect.yaml`, `buf.gen.ts.yaml`, `buf.gen.python.yaml`, `buf.gen.java.yaml`, `Makefile.example`.

Add a new sample by dropping a file here or in `assets/` and listing its basename in this file.
