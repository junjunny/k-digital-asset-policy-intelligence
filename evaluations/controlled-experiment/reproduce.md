# 재현 방법

```bash
python3 scripts/controlled_experiment.py init
python3 scripts/controlled_experiment.py environment
python3 scripts/controlled_experiment.py run --all
python3 scripts/controlled_experiment.py blind
python3 scripts/controlled_experiment.py aggregate
```

`run`은 Codex CLI 로그인을 필요로 하며 유료 API 키를 요구하지 않는다. CI는 live 실행을 하지 않고 manifest·resume·retry·usage parser·blind mapping·집계만 테스트한다.
