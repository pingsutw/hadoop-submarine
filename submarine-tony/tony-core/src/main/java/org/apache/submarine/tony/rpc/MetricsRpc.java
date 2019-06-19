/**
 * Copyright 2019 LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
 * See LICENSE in the project root for license information.
 */
package org.apache.submarine.tony.rpc;

import org.apache.submarine.tony.rpc.impl.MetricsWritable;
import org.apache.hadoop.ipc.VersionedProtocol;


public interface MetricsRpc extends VersionedProtocol {
  long versionID = 1L;

  void updateMetrics(String taskType, int taskIndex, MetricsWritable metrics);
}
