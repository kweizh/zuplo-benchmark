# Configure Datadog Logging Plugin in Zuplo

## Background
You have a Zuplo API project. You need to configure the gateway to push all logs to Datadog by adding the Datadog logging plugin to the runtime extensions.

## Requirements
- Create or update the `modules/zuplo.runtime.ts` file in your project.
- Implement the `runtimeInit` function to register the `DataDogLoggingPlugin`.
- Configure the plugin with the API key from the environment variable `DATADOG_API_KEY`.
- Set the `source` option to `zuplo-gateway`.
- Add a custom tag `env: production` to the `tags` option.

## Implementation Guide
1. Ensure you are in the `/home/user/myproject` directory.
2. Create a file at `modules/zuplo.runtime.ts`.
3. Import `RuntimeExtensions` and `DataDogLoggingPlugin` from `@zuplo/runtime`.
4. Export a function named `runtimeInit` that takes a `runtime: RuntimeExtensions` parameter.
5. Inside the function, call `runtime.addPlugin()` passing a new instance of `DataDogLoggingPlugin`.
6. Pass the required options object: `apiKey` (using `process.env.DATADOG_API_KEY`), `source`, and `tags`.

## Constraints
- Project path: `/home/user/myproject`