# Kubernetes (kubectl, Lens, k9s)

Runtime state of services: what is running, what restarted, what changed in the cluster. Lens and k9s show the same data as `kubectl`, in a UI.

## What this source holds

- Pods: restarts, exit reasons (`OOMKilled`, `CrashLoopBackOff`, `Error`), recent logs
- Events: scheduling failures, failed probes, image pull errors, evictions
- Deployments: rollout history, the image tag of each revision, replica counts
- Resource limits and requests, and autoscaler (HPA) decisions
- ConfigMaps (and the names, never the values, of Secrets)

## How to search it

All read-only. Confirm the context and the namespace before every command, and never run `apply`, `edit`, `delete`, `scale`, `rollout restart` or `exec` here.

```bash
kubectl config current-context
kubectl -n <ns> get pods -o wide
kubectl -n <ns> describe pod <pod>                 # last state, exit reason, events
kubectl -n <ns> get events --sort-by=.lastTimestamp | tail -50
kubectl -n <ns> logs <pod> --previous --since=2h  # logs of the crashed container
kubectl -n <ns> rollout history deploy/<name>
kubectl -n <ns> rollout history deploy/<name> --revision=<n>   # image and config of one revision
kubectl -n <ns> get hpa
kubectl -n <ns> top pods                           # needs metrics-server
```

In Lens or k9s, the same views are the pod detail, Events, and the deployment's revision list.

## What good evidence looks like

- An `OOMKilled` exit reason with a memory limit lower than the observed use
- A new rollout revision with a new image tag, right before the errors
- Failed readiness probes that removed pods from the load balancer

## Pitfalls

- **Events expire** after about an hour by default. Use the logging store for older ones.
- **`--previous`** only works while the old container is still recorded. Capture it early.
- **Secrets.** Never print Secret values, even in a describe output. Names only.
- **The wrong cluster.** Always state the context and namespace in the citation.

## What to return

Context, namespace, the object, the command run, the quoted lines (exit reason, event, revision), and the times in UTC.
