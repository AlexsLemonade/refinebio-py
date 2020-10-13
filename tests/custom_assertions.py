
class CustomAssertions:

    def assertObject(self, actual, expected):
        """Assert that a model is equivalent to its dict counterpart.

        Verifies that all properties have been set correctly
        Verifies that all set properties can be accessed by dot notation
        """

        # if expected is a dict and actual is some model object do the complicated logic
        if type(expected) is dict and type(actual) is not dict: 
            for key, value in expected.items():
                if type(value) is list:
                    if len(value) != len(getattr(actual, key)):
                        raise AssertionError(
                            "actual.{0} did not match expected value:\nexpected: {1} - length: {2}\nactual: {3} - length: {4}".format(
                                key,
                                value,
                                len(value),
                                getattr(actual, key),
                                len(getattr(actual, key))
                            )
                        )

                    for i in range(len(value)):
                        self.assertObject(getattr(actual, key)[i], value[i])

                elif type(value) is dict: 
                    self.assertObject(getattr(actual, key), value)

                else:
                    if getattr(actual, key) != value:
                        raise AssertionError(
                            "actual.{0} did not match expected value:\nexpected: {1}\nactual: {2}".format(
                                key,
                                value,
                                getattr(actual, key)
                            )
                        )

        # if we get here, actual and expected are both normal data types so just compare with ==
        else:
            if actual != expected:
                raise AssertionError(
                    "actual did not match expected value:\nexpected: {1}\nactual: {2}".format(
                        expected,
                        actual
                    )
                )
