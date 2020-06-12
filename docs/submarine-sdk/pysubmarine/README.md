<!---
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

# PySubmarine
PySubmarine is aiming to ease the ML engineer's life by providing a set of libraries.

It includes a high-level out-of-box ML library like deepFM, FM, etc.
low-level library to interact with submarine like creating experiment,
tracking experiment metrics, parameters.


## Package setup
- Clone repository
```bash
git clone https://github.com/apache/submarine.git
cd submarine/submarine-sdk/pysubmarine
```
- Install pip package
```bash
pip install .
```
- Run unit tests
```bash
pytest --cov=submarine -vs -m "not e2e"
```
- Run E2E tests

Before running e2e tests, user have to start submarine server locally
```bash
pytest --cov=submarine -vs -m "e2e"
```
- Run checkstyle
```bash
./submarine-sdk/pysubmarine/github-actions/lint.sh
```
## How to generate REST SDK from swagger
- [Generate REST SDK from swagger](./generate_api.md)

## Easy-to-use model trainers
- [FM](../../../submarine-sdk/pysubmarine/example/deepfm)
- [DeepFM](../../../submarine-sdk/pysubmarine/example/fm)

## Submarine experiment management
Makes it easy to run distributed or non-distributed TensorFlow, PyTorch experiments on Kubernetes.
- [mnist example](../../../submarine-sdk/pysubmarine/example/submarine_job_sdk.ipynb)

## PySubmarine API Reference
- [Tracking](tracking.md)
