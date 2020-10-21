
class CustomAssertions:

    def assertObject(self, actual, expected):
        """Assert that a model is equivalent to its dict counterpart.

        Verifies that all properties have been set correctly
        Verifies that all set properties can be accessed by dot notation
        """

        # if actual and expected are the same type, just compare with ==
        if type(actual) == type(expected):
            if actual != expected:
                raise AssertionError(
                    "actual did not match expected value:\nexpected: {1}\nactual: {2}".format(
                        expected,
                        actual
                    )
                )
            return


        # if we get here, actual is an model class object so do the complicated logic
        for key, value in expected.items():
            actual_value = getattr(actual, key)

            if type(value) is list:
                if len(value) != len(actual_value):
                    raise AssertionError(
                        "actual.{0} did not match expected value:\nexpected: {1} - length: {2}\nactual: {3} - length: {4}".format(
                            key,
                            value,
                            len(value),
                            actual_value,
                            len(actual_value)
                        )
                    )

                for i in range(len(value)):
                    self.assertObject(actual_value[i], value[i])

            elif type(value) is dict: 
                self.assertObject(actual_value, value)

            else:
                if actual_value != value:
                    raise AssertionError(
                        "actual.{0} did not match expected value:\nexpected: {1}\nactual: {2}".format(
                            key,
                            value,
                            actual_value
                        )
                    )
